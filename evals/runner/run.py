"""Prepare or execute matched cases; no auth copying, default no execution, no automatic wins."""
import argparse,hashlib,json,os,shutil,sys
from pathlib import Path
from supervisor import supervise,snapshot
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--execute',action='store_true');p.add_argument('--model');p.add_argument('--timeout',type=int,default=600);p.add_argument('--case');p.add_argument('--condition',choices=('baseline','scenello'));p.add_argument('--repetitions',type=int,default=2);a=p.parse_args();out=a.output.resolve()
 if not out.is_relative_to(ROOT/'artifacts'):p.error('output must remain in excluded artifacts')
 if not 1<=a.repetitions<=10 or a.timeout<1:p.error('invalid bounded run settings')
 for brief in sorted((ROOT/'evals/briefs').glob('*.md')):
  if a.case and brief.stem!=a.case:continue
  for condition in ((a.condition,) if a.condition else ('baseline','scenello')):
   for rep in range(1,a.repetitions+1):
    folder=out/brief.stem/f'{condition}-{rep:02}';folder.mkdir(parents=True,exist_ok=False);work=folder/'project';work.mkdir();home=folder/'cli-home';home.mkdir();raw=brief.read_bytes()
    if condition=='scenello':shutil.copytree(ROOT/'skills/scenello',work/'.agents/skills/scenello',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    before=snapshot(work);record={'case':brief.stem,'condition':condition,'run_id':rep,'prompt_sha256':hashlib.sha256(raw).hexdigest(),'starter_sha256':hashlib.sha256(json.dumps(before,sort_keys=True).encode()).hexdigest(),'starter_files':before,'model_requested':a.model or 'host default, observed identity must come from trace','activation':'not-tested','outcome':'INCOMPLETE','authentication':'No personal credentials copied. Supported authentication must be provided separately.','comparability':'Global skill/config isolation and equal tool policy must be verified, not assumed from a directory name.'}
    (folder/'record.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
    if a.execute:
     env=os.environ.copy();env['CODEX_HOME']=str(home);cmd=['codex','exec','--json','--skip-git-repo-check','-C',str(work)]
     if a.model:cmd+=['--model',a.model]
     result=supervise(cmd+['-'],work,folder/'execution',a.timeout,raw,env);record['execution_status']=result['status'];record['session_id']=result.get('session_id');(folder/'record.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
 print('Records prepared; actual traces and independent browser/creative validation determine outcomes. No comparisons assigned automatically.')
if __name__=='__main__':main()
