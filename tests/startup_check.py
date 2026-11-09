"""Audit startup traces for layout forced by scene/font-helper script evaluation.

The default fails on the measured regression. --allow-forced records a prior baseline.
Native frame layout and later callbacks are reported separately, not hidden or timed out.
"""
import argparse
import gzip
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directories',nargs='+',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--allow-forced',action='store_true')
    args=parser.parse_args();out=args.output.resolve()
    if not out.is_relative_to(ROOT/'artifacts'):parser.error('output must remain in excluded artifacts')
    records=[]
    for directory in args.directories:
        folder=directory.resolve()
        if not folder.is_relative_to(ROOT/'artifacts'):parser.error('traces must remain in excluded artifacts')
        for path in sorted(folder.glob('trace-*.json.gz')):
            events=json.loads(gzip.decompress(path.read_bytes()))['traceEvents']
            scripts=[e for e in events if e.get('name')=='EvaluateScript' and e.get('ph')=='X' and urlsplit(e.get('args',{}).get('data',{}).get('url','')).path.endswith(('/reading-ready.js','/observatory/scene.js','/materials/scene.js'))]
            assert len(scripts)==2,(path.name,'expected scene and font-helper evaluations',len(scripts))
            for script in scripts:
                end=script['ts']+script.get('dur',0)
                layouts=[e for e in events if e.get('name')=='Layout' and e.get('ph')=='X' and (e.get('pid'),e.get('tid'))==(script.get('pid'),script.get('tid')) and script['ts']<=e['ts'] and e['ts']+e.get('dur',0)<=end]
                records.append({'trace':folder.name+'/'+path.name,'script':urlsplit(script['args']['data']['url']).path,
                                'script_ms':round(script.get('dur',0)/1000,3),'nested_layouts':len(layouts),
                                'nested_layout_ms':round(sum(e.get('dur',0) for e in layouts)/1000,3)})
    assert records,'no startup script traces found'
    failures=[r for r in records if r['nested_layouts']]
    result={'scripts':len(records),'scripts_forcing_layout':len(failures),'nested_layout_ms':round(sum(r['nested_layout_ms'] for r in records),3),'records':records,
            'scope':'Only Layout nested within initial EvaluateScript for scene.js/reading-ready.js. This does not certify total frame cost or remove other startup samples.'}
    out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k not in ('records','scope')}))
    if failures and not args.allow_forced:raise SystemExit('FAIL: startup script evaluation forced layout')


if __name__=='__main__':main()
