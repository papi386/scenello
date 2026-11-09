"""Compare the current demos with a reviewed local release, without downloading assets.

Checks the same scroll poses, transforms, artwork, typography and real destinations.
The baseline archive is trusted local project output, not an arbitrary reference ZIP.
"""
import argparse
import functools
import hashlib
from http.server import ThreadingHTTPServer
import json
import os
from pathlib import Path
import threading
import zipfile

from browser_check import ROOT, QuietHandler

POSE = """() => [...document.querySelectorAll('.hero-copy,.statement,.optics,.core,.study,.fan,.sample')].map(e=>{
 const s=getComputedStyle(e),r=e.getBoundingClientRect();return {class:e.className,transform:s.transform,
 opacity:s.opacity,color:s.color,font:s.font,fontFamily:s.fontFamily,inert:e.inert,
 rect:[r.x,r.y,r.width,r.height],href:e.getAttribute('href'),html:e.innerHTML};})"""


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--baseline',type=Path,required=True)
    p.add_argument('--executable')
    p.add_argument('--output',type=Path,default=ROOT/'artifacts/cinematic-parity')
    p.add_argument('--catalogue-only',action='store_true',help='Compare fully traversed reading sections separately')
    args=p.parse_args()
    out=args.output.resolve()
    if not out.is_relative_to(ROOT/'artifacts'):p.error('output must remain in excluded artifacts')
    out.mkdir(parents=True,exist_ok=True)
    baseline=out/'baseline'
    with zipfile.ZipFile(args.baseline) as z:
        checksums=json.loads(z.read('release-checksums.json'))
        for name,sha in checksums.items():
            if not name.startswith('skills/scenello/assets/examples/'):
                continue
            target=(baseline/Path(name).relative_to('skills/scenello/assets/examples')).resolve()
            if not target.is_relative_to(baseline.resolve()):
                raise ValueError('baseline escaped evidence folder')
            data=z.read(name)
            assert hashlib.sha256(data).hexdigest()==sha
            target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    from playwright.sync_api import sync_playwright
    from PIL import Image,ImageChops
    servers=[];urls=[]
    for directory in (baseline,ROOT/'skills/scenello/assets/examples'):
        server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(directory)))
        threading.Thread(target=server.serve_forever,daemon=True).start();servers.append(server)
        urls.append(f'http://127.0.0.1:{server.server_port}')
    results=[];original=Path.cwd();os.chdir(out)
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(**({'executable_path':args.executable} if args.executable else {}))
            for demo in ('observatory','materials'):
                for width,height in ((320,844),(360,800),(375,812),(390,844),(430,932),(768,1024),(1024,768),(1280,800),(1440,900),(1920,1080),(2560,1440),(844,390)):
                    ctx=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=2 if width<768 else 1,is_mobile=width<768 or (width,height)==(844,390),has_touch=width<768 or (width,height)==(844,390))
                    pages=[ctx.new_page(),ctx.new_page()]
                    for page,url in zip(pages,urls):
                        page.goto(f'{url}/{demo}/');page.evaluate('document.fonts.ready');page.wait_for_timeout(80)
                    max_delta=0;pixel_max=0
                    points=sorted(set([i/20 for i in range(21)]+[.249,.251,.26,.28,.31,.37,.4]))
                    for step,progress in (() if args.catalogue_only else enumerate(points)):
                        for page in pages:
                            page.evaluate("p=>{const s=document.querySelector('.journey,.sequence');scrollTo({top:s.offsetTop+p*(s.offsetHeight-document.querySelector('.stage').offsetHeight),behavior:'instant'})}",progress)
                            page.wait_for_timeout(40)
                        old,new=[page.evaluate(POSE) for page in pages]
                        assert len(old)==len(new)
                        for a,b in zip(old,new):
                            transparent=float(a['opacity'])==0 and float(b['opacity'])==0
                            for field in ('class','transform','opacity','color','font','fontFamily','inert','href','html'):
                                if field=='transform' and transparent:continue
                                assert a[field]==b[field],(demo,width,progress,field,a[field],b[field])
                            delta=0 if transparent else max(abs(x-y) for x,y in zip(a['rect'],b['rect']));max_delta=max(max_delta,delta)
                            assert delta<.01,(demo,width,progress,'geometry',delta)
                        if width in (390,1440) and progress in (0,.249,.251,.26,.35,.65,1):
                            files=[out/f'{demo}-{width}-{step}-{kind}.png' for kind in ('before','after')]
                            for page,file in zip(pages,files):page.screenshot(path=str(file))
                            a,b=[Image.open(file).convert('RGB') for file in files]
                            diff=ImageChops.difference(a,b);pixels=diff.get_flattened_data() if hasattr(diff,'get_flattened_data') else diff.getdata();ratio=0 if diff.getbbox() is None else sum(any(px) for px in pixels)/(a.width*a.height)
                            pixel_max=max(pixel_max,ratio)
                            assert ratio<.0001,(demo,width,progress,'changed-pixel-ratio',ratio)
                    if args.catalogue_only:
                        for page in pages:
                            # Traverse every real item so remembered intrinsic sizes are actual sizes.
                            for item in page.locator('article').all():
                                item.scroll_into_view_if_needed();page.wait_for_timeout(50)
                            page.evaluate("document.querySelector('#catalogue,#research').scrollIntoView({block:'start',behavior:'instant'})")
                            page.wait_for_timeout(100)
                        def reading(page):
                            return page.evaluate("""() => [...document.querySelectorAll('article,h2,.catalogue-head,.section-heading')].map(e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return {text:e.textContent,rect:[r.x,r.y,r.width,r.height],color:s.color,font:s.font};})""")
                        old,new=[reading(page) for page in pages]
                        for a,b in zip(old,new):
                            assert a['text']==b['text'] and a['font']==b['font'] and a['color']==b['color']
                            delta=max(abs(x-y) for x,y in zip(a['rect'],b['rect']));max_delta=max(max_delta,delta)
                            assert delta<.01,(demo,width,'catalogue-geometry',delta)
                        if width in (390,1440):
                            files=[out/f'{demo}-{width}-catalogue-{kind}.png' for kind in ('before','after')]
                            for page,file in zip(pages,files):page.screenshot(path=str(file))
                            a,b=[Image.open(file).convert('RGB') for file in files]
                            diff=ImageChops.difference(a,b);pixels=diff.get_flattened_data() if hasattr(diff,'get_flattened_data') else diff.getdata();ratio=0 if diff.getbbox() is None else sum(any(px) for px in pixels)/(a.width*a.height)
                            pixel_max=max(pixel_max,ratio)
                            assert ratio<.0001,(demo,width,'catalogue-pixel-ratio',ratio)
                    results.append({'demo':demo,'viewport':[width,height],'poses':0 if args.catalogue_only else len(points),'catalogue':args.catalogue_only,'max_geometry_delta_px':max_delta,'max_changed_pixel_ratio':pixel_max})
                    ctx.close()
            browser.close()
    finally:
        for server in servers:server.shutdown()
        os.chdir(original)
    (out/('catalogue-results.json' if args.catalogue_only else 'results.json')).write_bytes((json.dumps({'comparison':'Compare all properties except layout/matrix of fully zero-opacity nodes; opacity, content and interactivity still checked. Extra activation-boundary screenshots are mandatory.', 'baseline_sha256':hashlib.sha256(args.baseline.read_bytes()).hexdigest(),'checks':results},indent=2)+'\n').encode())
    print(json.dumps({'configurations':len(results),'poses':sum(r['poses'] for r in results),'max_changed_pixel_ratio':max(r['max_changed_pixel_ratio'] for r in results),'result':'PASS'}))


if __name__=='__main__':main()
