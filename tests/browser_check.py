"""Local-only browser checks and optional repeated lab measurements. No auto install.

python tests/browser_check.py [--runs 10] [--executable /path/to/chromium]
Raw artifacts stay under ignored artifacts/. Use an existing Playwright installation.
"""
import argparse
import functools
import gzip
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def native_eval(cdp, expression, await_promise=False):
    """Avoid injecting Playwright's large utility bundle into a measured document."""
    response=cdp.send('Runtime.evaluate',{'expression':expression,'returnByValue':True,
                                        'awaitPromise':await_promise,'timeout':10000})
    if response.get('exceptionDetails'):
        raise RuntimeError(response['exceptionDetails'])
    return response.get('result',{}).get('value')


def first_content(cdp):
    # A tiny native observer; wait_for_function would inject ~329 KB during startup.
    return native_eval(cdp,"""new Promise(resolve=>{
      if(performance.getEntriesByType('paint').some(e=>e.name==='first-contentful-paint')){resolve(true);return}
      const observer=new PerformanceObserver(list=>{
       if(list.getEntries().some(e=>e.name==='first-contentful-paint')){observer.disconnect();resolve(true)}
      });observer.observe({type:'paint',buffered:true});
    })""",True)


def native_click(cdp, selector):
    quoted=json.dumps(selector)
    native_eval(cdp,f"document.querySelector({quoted}).scrollIntoView({{block:'center',behavior:'instant'}})")
    native_eval(cdp,'new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(()=>resolve(true))))',True)
    point=native_eval(cdp,f"(()=>{{const r=document.querySelector({quoted}).getBoundingClientRect();return {{x:r.x+r.width/2,y:r.y+r.height/2}}}})()")
    cdp.send('Input.dispatchMouseEvent',{'type':'mousePressed',**point,'button':'left','clickCount':1})
    cdp.send('Input.dispatchMouseEvent',{'type':'mouseReleased',**point,'button':'left','clickCount':1})


def percentiles(values):
    ordered = sorted(values)
    return {f"p{p}": round(ordered[max(0, math.ceil(p/100*len(ordered))-1)], 3)
            if ordered else None for p in (50, 95, 99)}


INSTRUMENT = """(() => {
 const data=window.lab={intervals:[],timestamps:[],longFrames:[],longTasks:[],lcp:null,cls:0};
 let last=null,active=true,frame;
 function tick(t){if(last!==null){data.intervals.push(t-last);data.timestamps.push(t)}last=t;if(active)frame=requestAnimationFrame(tick)}
 frame=requestAnimationFrame(tick);
 const observers=[];
 for(const [type,key] of [['long-animation-frame','longFrames'],['longtask','longTasks'],['largest-contentful-paint','lcp'],['layout-shift','cls']]){
  if(!PerformanceObserver.supportedEntryTypes.includes(type))continue;
  const o=new PerformanceObserver(list=>{for(const e of list.getEntries()){
   if(key==='cls'){if(!e.hadRecentInput)data.cls+=e.value}
   else if(key==='lcp')data.lcp=e.startTime;
   else data[key].push(e.duration);
  }});o.observe({type,buffered:true});observers.push(o);
 }
 window.stopLab=()=>{active=false;cancelAnimationFrame(frame);observers.forEach(o=>o.disconnect());data.paint=performance.getEntriesByType('paint').map(e=>({name:e.name,ms:e.startTime}));data.resources=performance.getEntriesByType('resource').map(e=>({name:new URL(e.name).pathname,transfer:e.transferSize,decoded:e.decodedBodySize}));return data};
})();"""


def trace_tasks(events):
    # Only complete outer scheduler tasks on renderer main threads; don't count nested work twice.
    main = {(e.get("pid"), e.get("tid")) for e in events
            if e.get("name") == "thread_name" and e.get("args", {}).get("name") == "CrRendererMain"}
    spans = sorted((e["ts"], e["ts"]+e["dur"]) for e in events
                   if (e.get("pid"), e.get("tid")) in main and e.get("ph") == "X"
                   and e.get("name") in ("RunTask", "ThreadControllerImpl::RunTask") and e.get("dur", 0) > 0)
    merged = []
    for a, b in spans:
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(b, merged[-1][1])
        else:
            merged.append([a, b])
    values = [(b-a)/1000 for a, b in merged]
    return {"metric": "top-level renderer task duration, not frame workload", "samples": len(values),
            "ms": percentiles(values), "over_16ms": sum(x > 16 for x in values),
            "max_ms": round(max(values, default=0), 3)}


def finish_trace(cdp, complete, target):
    cdp.send("Tracing.end")
    deadline = time.monotonic()+15
    while not complete and time.monotonic() < deadline:
        cdp.send("Runtime.evaluate", {"expression": "0"})
        time.sleep(.03)
    if not complete:
        raise RuntimeError("trace stream did not complete")
    handle = complete[0]["stream"]
    parts = []
    while True:
        data = cdp.send("IO.read", {"handle": handle})
        parts.append(data.get("data", ""))
        if data.get("eof"):
            break
    cdp.send("IO.close", {"handle": handle})
    raw = "".join(parts)
    with gzip.open(target, "wt", encoding="utf-8") as f:
        f.write(raw)
    return trace_tasks(json.loads(raw).get("traceEvents", []))


def main():
    global OUT
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--runs", type=int, default=0)
    p.add_argument("--executable")
    p.add_argument("--skip-checks",action="store_true",help="Measure only; retain functional results separately")
    p.add_argument("--mode",choices=("static","motion"),help="Measure only this mode")
    p.add_argument("--cache",choices=("mixed","cold","warm"),default="mixed")
    p.add_argument("--output",type=Path,default=OUT)
    args = p.parse_args()
    OUT=args.output.resolve()
    if not OUT.is_relative_to(ROOT/"artifacts"):
        p.error("raw test output must remain in the excluded artifacts directory")
    if not 0 <= args.runs <= 30:
        p.error("runs must be 0..30")
    from playwright.sync_api import sync_playwright
    OUT.mkdir(exist_ok=True)
    original_cwd=Path.cwd()
    # Chromium driver diagnostics sometimes ignore --log-file on Windows.
    # Start the driver inside the excluded evidence directory as well.
    os.chdir(OUT)
    server = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(ROOT / "skills/scenello/assets/examples")))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}"
    results = {"environment": {"os": platform.system()+" "+platform.release(), "python": platform.python_version(),
              "playwright": importlib.metadata.version("playwright"), "network": "loopback, no network throttle",
              "percentiles": "nearest rank", "physical_device": False}, "checks": [], "measurements": []}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=["--log-file="+str(OUT/"chromium.log")], **({"executable_path": args.executable} if args.executable else {}))
            results["environment"]["browser"] = browser.version
            for demo in (() if args.skip_checks else ("observatory", "materials")):
                for width in (320,360,375,390,430,768,1024,1280,1440,1920,2560):
                    context = browser.new_context(viewport={"width": width, "height": 844 if width<768 else 900},
                                                  is_mobile=width<768, has_touch=width<768, device_scale_factor=2 if width<768 else 1)
                    page = context.new_page()
                    errors = []
                    page.on("pageerror", lambda e: errors.append(str(e)))
                    page.goto(f"{base}/{demo}/")
                    page.wait_for_function("document.documentElement.classList.contains('motion')")
                    for progress in (0,.35,.65,1):
                        page.evaluate("p=>{const s=document.querySelector('.journey,.sequence');scrollTo({top:s.offsetTop+p*(s.offsetHeight-document.querySelector('.stage').offsetHeight),behavior:'instant'})}", progress)
                        page.wait_for_timeout(70)
                        assert page.evaluate("document.documentElement.scrollWidth<=innerWidth"), (demo,width,progress,"overflow")
                        if width in (390,1440):
                            page.screenshot(path=str(OUT/f"{demo}-{width}-{progress}.png"))
                    page.locator("#catalogue" if demo=="materials" else "#research").scroll_into_view_if_needed()
                    if demo == "materials":
                        page.get_by_role("button",name="Metal",exact=True).click()
                        assert page.locator("article:visible").count()==2
                        page.get_by_role("button",name="All materials",exact=True).click()
                    page.locator("summary").first.click()
                    assert page.locator("details").first.get_attribute("open") is not None
                    assert not errors, errors
                    results["checks"].append({"demo":demo,"width":width,"motion_stages":4,"functional":True})
                    context.close()
                for reduced,js in ((True,True),(False,False)):
                    context=browser.new_context(viewport={"width":390,"height":844},reduced_motion="reduce" if reduced else "no-preference",java_script_enabled=js)
                    page=context.new_page();page.goto(f"{base}/{demo}/")
                    assert page.locator("h1").is_visible()
                    assert page.locator("article").count()>=3
                    assert not page.evaluate("document.documentElement.classList.contains('motion')")
                    context.close()
                # Landscape, resize mid-motion, direct detail and keyboard skip.
                context=browser.new_context(viewport={"width":844,"height":390},has_touch=True)
                page=context.new_page();page.goto(f"{base}/{demo}/");page.keyboard.press("Tab")
                assert page.locator(".skip").evaluate("e=>e===document.activeElement")
                page.keyboard.press("Enter");page.wait_for_timeout(80)
                page.set_viewport_size({"width":360,"height":780})
                assert page.evaluate("document.documentElement.scrollWidth<=innerWidth")
                context.close()
            for demo in ("observatory","materials"):
                for profile,width,height,cpu,dpr in (("laptop",1440,900,1,1),("mobile-emulated",390,844,4,2)):
                    for mode in ((args.mode,) if args.mode else ("static","motion")):
                        context=browser.new_context(viewport={"width":width,"height":height},has_touch=width<768,is_mobile=width<768,device_scale_factor=dpr)
                        context.add_init_script(INSTRUMENT)
                        if args.cache=="warm":
                            prime=context.new_page()
                            prime.goto(f"{base}/{demo}/"+("?static" if mode=="static" else ""))
                            prime.wait_for_timeout(150)
                            prime.close()
                        for run in range(args.runs):
                            page=context.new_page();cdp=context.new_cdp_session(page)
                            cdp.send("Emulation.setCPUThrottlingRate",{"rate":cpu})
                            cdp.send("Network.enable")
                            if run==0 or args.cache=="cold":
                                if args.cache!="warm":cdp.send("Network.clearBrowserCache")
                            complete=[];cdp.on("Tracing.tracingComplete",lambda event:complete.append(event))
                            cdp.send("Tracing.start",{"categories":"devtools.timeline,toplevel,blink.user_timing","transferMode":"ReturnAsStream"})
                            page.goto(f"{base}/{demo}/"+("?static" if mode=="static" else ""))
                            page.wait_for_timeout(200)
                            cdp.send("Input.synthesizeScrollGesture",{"x":int(width*.5),"y":int(height*.7),"yDistance":-int(height*1.6),"speed":900,"gestureSourceType":"mouse"})
                            page.wait_for_timeout(150)
                            data=native_eval(cdp,"stopLab()")
                            data["trace"]=finish_trace(cdp,complete,OUT/f"trace-{demo}-{profile}-{mode}-{run}.json.gz")
                            intervals=data.pop("intervals")
                            data["raf_interval_end_ms"]=data.pop("timestamps")
                            data.update({"demo":demo,"profile":profile,"mode":mode,"run":run,"cache":args.cache if args.cache!="mixed" else "cold" if run==0 else "warm","cpu_throttle":cpu,"viewport":[width,height],"dpr":dpr,"raf_samples":len(intervals),"raf_intervals_ms":intervals,"raf_ms":percentiles(intervals),"first_raf_interval_ms":round(intervals[0],3) if intervals else None,"raf_over_ms":{str(t):sum(x>t for x in intervals) for t in (16.67,33.3,50)},"scroll_y":native_eval(cdp,"scrollY")})
                            results["measurements"].append(data)
                            page.close()
                        context.close()
            browser.close()
    finally:
        server.shutdown()
        (OUT/"browser-results.json").write_text(json.dumps(results,indent=2),encoding="utf-8")
        os.chdir(original_cwd)
    print(json.dumps({"responsive_checks":len(results["checks"]),"measurements":len(results["measurements"]),"browser":results["environment"].get("browser")}))


if __name__=="__main__":
    main()
