"""Additional Chromium interaction, emulated-touch and original-diagram checks."""
import argparse
import functools
from http.server import ThreadingHTTPServer
import json
import os
from pathlib import Path
import threading
from browser_check import ROOT, OUT, QuietHandler


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--executable");args=p.parse_args()
    from playwright.sync_api import sync_playwright
    OUT.mkdir(exist_ok=True)
    original_cwd=Path.cwd();os.chdir(OUT)
    server=ThreadingHTTPServer(("127.0.0.1",0),functools.partial(QuietHandler,directory=str(ROOT/"skills/scenello/assets")))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f"http://127.0.0.1:{server.server_port}"
    checks=[]
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(**({"executable_path":args.executable} if args.executable else {}))
            for demo in ("observatory","materials"):
                context=browser.new_context(viewport={"width":390,"height":844},is_mobile=True,has_touch=True,device_scale_factor=2)
                context.add_init_script("window.sceneFrames=0;const native=requestAnimationFrame;window.requestAnimationFrame=fn=>native(t=>{window.sceneFrames++;fn(t)})")
                page=context.new_page();page.goto(f"{base}/examples/{demo}/")
                page.wait_for_timeout(200);before=page.evaluate("sceneFrames");page.wait_for_timeout(400)
                assert page.evaluate("sceneFrames")==before, "scene loops continuously while idle"
                cdp=context.new_cdp_session(page)
                cdp.send("Input.dispatchTouchEvent",{"type":"touchStart","touchPoints":[{"x":195,"y":700}]})
                for y in range(670,149,-40):
                    cdp.send("Input.dispatchTouchEvent",{"type":"touchMove","touchPoints":[{"x":195,"y":y}]})
                    page.wait_for_timeout(17)
                cdp.send("Input.dispatchTouchEvent",{"type":"touchEnd","touchPoints":[]})
                page.wait_for_timeout(150)
                assert page.evaluate("scrollY")>50, "emulated touch did not scroll"
                assert float(page.locator(".stage").get_attribute("data-progress"))>0, "touch did not drive scene"
                checks.append({"demo":demo,"emulated_touch_scroll_y":page.evaluate("scrollY"),"idle_raf_stopped":True})
                # Continuous seek/reverse and resize use the production scroll renderer.
                for progress in (.85,.249,.251,.249,.26,.85):
                    page.evaluate("p=>{const s=document.querySelector('.journey,.sequence');scrollTo({top:s.offsetTop+p*(s.offsetHeight-document.querySelector('.stage').offsetHeight),behavior:'instant'})}",progress)
                    page.wait_for_timeout(80)
                    actual=float(page.locator(".stage").get_attribute("data-progress"))
                    assert abs(actual-progress)<.005,(actual,progress)
                page.set_viewport_size({"width":844,"height":390});page.wait_for_timeout(70)
                assert page.evaluate("document.documentElement.scrollWidth<=innerWidth")
                page.emulate_media(reduced_motion="reduce");page.wait_for_timeout(70)
                assert not page.evaluate("document.documentElement.classList.contains('motion')")
                page.emulate_media(reduced_motion="no-preference");page.wait_for_timeout(70)
                assert page.evaluate("document.documentElement.classList.contains('motion')")
                # A cancelled queued frame must not block scheduling after a lifecycle restore.
                page.evaluate("""() => {dispatchEvent(new Event('scroll'));dispatchEvent(new PageTransitionEvent('pagehide',{persisted:true}));dispatchEvent(new PageTransitionEvent('pageshow',{persisted:true}))}""")
                page.evaluate("() => {const s=document.querySelector('.journey,.sequence');scrollTo({top:s.offsetTop+.5*(s.offsetHeight-document.querySelector('.stage').offsetHeight),behavior:'instant'})}")
                page.wait_for_timeout(80)
                assert abs(float(page.locator('.stage').get_attribute('data-progress'))-.5)<.005
                checks[-1]['synthetic_lifecycle_restore']=True
                # Ordinary destinations survive navigation and history.
                target="aluminium" if demo=="materials" else "interference"
                page.goto(f"{base}/examples/{demo}/#{target}")
                assert page.locator('#'+target).is_visible()
                page.goto(f"{base}/examples/");page.go_back();assert page.locator('#'+target).is_visible()
                if demo=="materials":
                    page.goto(f"{base}/examples/materials/#%ZZ");assert page.locator('h1').is_visible()
                context.close()
            for demo in ("observatory","materials"):
                fallback=browser.new_context(viewport={"width":390,"height":844})
                fallback.route("**/*.woff",lambda route:route.abort())
                fallback.route("**/optical-aperture.svg",lambda route:route.abort())
                probe=fallback.new_page();probe.goto(f"{base}/examples/{demo}/")
                assert probe.locator('h1').is_visible()
                probe.locator('#research' if demo=='observatory' else '#catalogue').scroll_into_view_if_needed()
                probe.locator('summary').first.click()
                assert probe.locator('details').first.get_attribute('open') is not None
                fallback.close()
            # A missing critical subset must use the unchanged complete local font.
            for demo in ('observatory','materials'):
                fallback=browser.new_context(viewport={'width':390,'height':844})
                fallback.route('**/*critical*.woff',lambda route:route.abort())
                probe=fallback.new_page();probe.goto(f'{base}/examples/{demo}/')
                probe.evaluate('document.fonts.ready')
                assert probe.locator('h1').is_visible()
                assert probe.evaluate("Array.from(document.fonts).some(f=>f.family.includes('Scenello UI')&&f.status==='loaded')")
                assert probe.evaluate("performance.getEntriesByType('resource').some(e=>/scenello-ui-(regular|bold)\\.woff/.test(e.name))")
                fallback.close()
            page=browser.new_page(viewport={"width":1120,"height":360})
            names=[p.stem for p in sorted((ROOT/"skills/scenello/assets/storyboards").glob("*.svg"))]
            for name in names:
                page.goto(f"{base}/storyboards/{name}.svg");page.screenshot(path=str(OUT/f"storyboard-{name}.png"))
            browser.close()
    finally:server.shutdown();os.chdir(original_cwd)
    (OUT/"interaction-results.json").write_text(json.dumps(checks,indent=2),encoding="utf-8")
    print(json.dumps({"demos":len(checks),"emulated_touch":"PASS","reverse_resize_history_reduced_motion":"PASS","storyboards_captured":len(names)}))


if __name__=="__main__":main()
