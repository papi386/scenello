"""Cold-load, fast-scroll/reverse, full-catalogue, rotation and interaction stress.

Uses existing Playwright/Chromium only. Raw diagnostics remain excluded artifacts.
Run paired with/without --trace; neither emulation nor rAF proves presented frames.
"""
import argparse
import functools
from http.server import ThreadingHTTPServer
import json
import os
from pathlib import Path
import threading

from browser_check import ROOT, QuietHandler, INSTRUMENT, percentiles, finish_trace, native_eval, first_content, native_click

PROFILES={
    'mobile':(390,844,2,4),
    'small-high-dpr':(320,740,3,4),
    'landscape':(844,390,2,4),
    'heavy-mobile':(390,844,3,6),
    'laptop':(1440,900,1,1),
    'constrained-network':(390,844,2,4),
}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runs',type=int,default=10)
    parser.add_argument('--profiles',nargs='+',choices=PROFILES,default=['mobile','small-high-dpr','landscape','heavy-mobile','laptop','constrained-network'])
    parser.add_argument('--trace',action='store_true')
    parser.add_argument('--executable')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if not 1<=args.runs<=30:parser.error('runs must be 1..30')
    out=args.output.resolve()
    if not out.is_relative_to(ROOT/'artifacts'):parser.error('output must be in excluded artifacts')
    out.mkdir(parents=True,exist_ok=True);original=Path.cwd();os.chdir(out)
    from playwright.sync_api import sync_playwright
    server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT/'skills/scenello/assets/examples')))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}'
    result={'environment':{'cache':'cold HTTP cache each run','network':'loopback; only constrained-network profile uses 120 ms and 200000/96000 bytes per second','trace':args.trace,'physical_device':False,'percentiles':'nearest rank'},'runs':[]}
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(**({'executable_path':args.executable} if args.executable else {}))
            result['environment']['browser']=browser.version
            for demo in ('observatory','materials'):
                for name in args.profiles:
                    width,height,dpr,cpu=PROFILES[name]
                    for run in range(args.runs):
                        ctx=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=dpr,is_mobile=width<900,has_touch=True)
                        ctx.add_init_script(INSTRUMENT)
                        ctx.add_init_script("window.stress={phase:'load',events:[]};addEventListener('error',e=>stress.events.push(e.message))")
                        page=ctx.new_page();cdp=ctx.new_cdp_session(page)
                        cdp.send('Emulation.setCPUThrottlingRate',{'rate':cpu});cdp.send('Network.enable');cdp.send('Network.clearBrowserCache')
                        if name=='constrained-network':cdp.send('Network.emulateNetworkConditions',{'offline':False,'latency':120,'downloadThroughput':200000,'uploadThroughput':96000})
                        complete=[]
                        if args.trace:
                            cdp.on('Tracing.tracingComplete',lambda e:complete.append(e))
                            cdp.send('Tracing.start',{'categories':'devtools.timeline,toplevel,blink.user_timing','transferMode':'ReturnAsStream'})
                        page.goto(f'{base}/{demo}/',wait_until='commit')
                        first_content(cdp)
                        phases=[]
                        def phase(label):
                            phases.append({'name':label,'start_ms':native_eval(cdp,'performance.now()')})
                        def gesture(distance,speed):
                            cdp.send('Input.synthesizeScrollGesture',{'x':width//2,'y':int(height*.7),'yDistance':distance,'speed':speed,'gestureSourceType':'mouse'})
                        # No warmup delay before the first input: this includes startup contention.
                        phase('fast-forward');gesture(-int(height*2),3200)
                        phase('reverse');gesture(int(height),2400)
                        phase('catalogue');gesture(-6500,6500)
                        target='#catalogue' if demo=='materials' else '#research'
                        native_eval(cdp,"document.querySelector("+json.dumps(target)+").scrollIntoView({block:'start',behavior:'instant'})")
                        phase('interaction')
                        if demo=='materials':
                            native_click(cdp,'[data-filter=metal]')
                            assert native_eval(cdp,"document.querySelectorAll('article:not([hidden])').length")==2
                            native_click(cdp,'[data-filter=all]')
                        native_click(cdp,'summary')
                        assert native_eval(cdp,"document.querySelector('details').open")
                        phase('orientation')
                        page.set_viewport_size({'width':height,'height':width});page.wait_for_timeout(80)
                        page.set_viewport_size({'width':width,'height':height});page.wait_for_timeout(80)
                        assert native_eval(cdp,'document.documentElement.scrollWidth<=innerWidth')
                        phase('return');gesture(int(native_eval(cdp,'scrollY'))+height,6000);page.wait_for_timeout(150)
                        assert native_eval(cdp,"document.querySelector('h1').getClientRects().length>0")
                        assert native_eval(cdp,'scrollY')<5, 'return gesture did not reach opening'
                        assert not native_eval(cdp,'stress.events')
                        data=native_eval(cdp,'stopLab()');intervals=data.pop('intervals');timestamps=data.pop('timestamps',[])
                        phase_stats={}
                        for i,(interval,end) in enumerate(zip(intervals,timestamps)):
                            label=next((mark['name'] for mark in reversed(phases) if end>=mark['start_ms']),'load')
                            phase_stats.setdefault(label,[]).append(interval)
                        data['phase_raf_ms']={key:{'samples':len(values),'ms':percentiles(values),'over_25ms':sum(x>25 for x in values),'max_ms':max(values)} for key,values in phase_stats.items()}
                        if args.trace:data['trace']=finish_trace(cdp,complete,out/f'{demo}-{name}-{run}.json.gz')
                        data.update({'demo':demo,'profile':name,'run':run,'viewport':[width,height],'dpr':dpr,'cpu_throttle':cpu,'input':'native synthesized wheel; touch dispatch checked separately','phases':phases,'first_interval_ms':intervals[0] if intervals else None,'raf_intervals_ms':intervals,'raf_ms':percentiles(intervals),'over_25ms':sum(x>25 for x in intervals),'over_50ms':sum(x>50 for x in intervals),'max_interval_ms':max(intervals,default=0),'functional':'PASS'})
                        result['runs'].append(data)
                        ctx.close()
                    print(json.dumps({'demo':demo,'profile':name,'runs':args.runs}),flush=True)
            browser.close()
    finally:
        server.shutdown();os.chdir(original)
        (out/'results.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({'runs':len(result['runs']),'trace':args.trace,'functional':'PASS'}))


if __name__=='__main__':main()
