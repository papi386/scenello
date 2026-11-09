"""Counterbalanced 0.2.0/current mobile startup comparison after parity extraction.

Uses the verified baseline folder produced by cinematic_parity.py. Raw results private.
"""
import argparse
import functools
from http.server import ThreadingHTTPServer
import json
import os
from pathlib import Path
import threading

from browser_check import ROOT,QuietHandler,INSTRUMENT,percentiles,finish_trace,native_eval


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--executable')
    p.add_argument('--baseline-dir',type=Path,default=ROOT/'artifacts/cinematic-parity/baseline')
    p.add_argument('--output',type=Path,default=ROOT/'artifacts/v3-paired')
    args=p.parse_args()
    baseline=args.baseline_dir.resolve()
    if not baseline.is_relative_to(ROOT/'artifacts'):p.error('baseline must be reviewed evidence within artifacts')
    if not (baseline/'materials/index.html').is_file():p.error('run the verified parity extraction first')
    out=args.output.resolve()
    if not out.is_relative_to(ROOT/'artifacts'):p.error('output must remain in artifacts')
    out.mkdir(parents=True,exist_ok=True)
    servers=[];urls={}
    for name,directory in [('previous',baseline),('current',ROOT/'skills/scenello/assets/examples')]:
        s=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(directory)))
        threading.Thread(target=s.serve_forever,daemon=True).start();servers.append(s);urls[name]=f'http://127.0.0.1:{s.server_port}'
    from playwright.sync_api import sync_playwright
    original=Path.cwd();os.chdir(out);results=[]
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(**({'executable_path':args.executable} if args.executable else {}))
            for demo in ('observatory','materials'):
                for pair in range(10):
                    order=('previous','current') if pair%2==0 else ('current','previous')
                    for version in order:
                        ctx=browser.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True)
                        ctx.add_init_script(INSTRUMENT);page=ctx.new_page();cdp=ctx.new_cdp_session(page)
                        cdp.send('Emulation.setCPUThrottlingRate',{'rate':4});cdp.send('Network.enable');cdp.send('Network.clearBrowserCache')
                        complete=[];cdp.on('Tracing.tracingComplete',lambda e:complete.append(e))
                        cdp.send('Tracing.start',{'categories':'devtools.timeline,toplevel,blink.user_timing','transferMode':'ReturnAsStream'})
                        page.goto(f'{urls[version]}/{demo}/');page.wait_for_timeout(200)
                        cdp.send('Input.synthesizeScrollGesture',{'x':195,'y':590,'yDistance':-1350,'speed':900,'gestureSourceType':'mouse'})
                        page.wait_for_timeout(150);data=native_eval(cdp,'stopLab()')
                        data['trace']=finish_trace(cdp,complete,out/f'{demo}-{version}-{pair}.json.gz')
                        intervals=data.pop('intervals');data.pop('timestamps',None)
                        data.update({'demo':demo,'version':version,'pair':pair,'order':list(order),'raf_intervals_ms':intervals,'first_interval_ms':intervals[0],'raf_ms':percentiles(intervals)})
                        results.append(data);ctx.close()
                print(json.dumps({'demo':demo,'pairs':10}),flush=True)
            browser.close()
    finally:
        for s in servers:s.shutdown()
        os.chdir(original)
        (out/'results.json').write_bytes((json.dumps({'method':'counterbalanced alternating order, 390x844 DPR2 CPU4x, HTTP cold, same traced input sequence','runs':results},indent=2)+'\n').encode())
    print(json.dumps({'runs':len(results),'pairs':len(results)//2}))


if __name__=='__main__':main()
