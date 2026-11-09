"""Opt-in local observable-action log. No hooks, uploads, transcript or environment capture."""
import argparse,datetime,hashlib,json,os,re,threading,time
from pathlib import Path
_LOCK=threading.Lock()
_SENSITIVE=re.compile(r'(?i)token|password|authorization|cookie|api.?key|secret|^(?:prompt|reasoning|transcript|environment)(?:$|_text|_content)')
def redact(value,workspace=None):
 if isinstance(value,dict):return {k:('[REDACTED]' if _SENSITIVE.search(k) else redact(v,workspace)) for k,v in value.items()}
 if isinstance(value,list):return [redact(v,workspace) for v in value]
 if not isinstance(value,str):return value
 if workspace:value=value.replace(str(workspace),'<workspace>').replace(Path(workspace).as_posix(),'<workspace>')
 home=Path.home();value=value.replace(str(home),'<home>').replace(home.as_posix(),'<home>')
 value=re.sub(r'(?i)(?:Bearer\s+|sk-|gh[pousr]_)[A-Za-z0-9_.-]{12,}','[REDACTED]',value)
 value=re.sub(r'(?i)(password|access_token|api_key)(\s*[:=]\s*)[^\s,;]+',r'\1\2[REDACTED]',value)
 return value
class Recorder:
 def __init__(self,directory,run_id,actor='agent',workspace=None):
  if not re.fullmatch(r'[A-Za-z0-9_-]{1,100}',run_id):raise ValueError('use a safe run identifier')
  self.folder=Path(directory).resolve()/run_id;self.folder.mkdir(parents=True,exist_ok=True);self.path=self.folder/'events.jsonl';self.actor=actor;self.workspace=workspace
 def append(self,event_type,phase='work',**data):
  protected={'schema_version','run_id','seq','timestamp_utc','actor','phase','event_type','previous_sha256','event_sha256','monotonic_ns','cwd'}
  if protected.intersection(data):raise ValueError('audit envelope fields cannot be overridden')
  with _LOCK,(self.folder/'append.lock').open('a+b') as lock:
   if os.name=='nt':
    import msvcrt
    lock.seek(0);lock.write(b'0');lock.flush();lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_LOCK,1)
   else:
    import fcntl
    fcntl.flock(lock,fcntl.LOCK_EX)
   try:
    previous=None
    if self.path.exists():
     for line in self.path.read_text(encoding='utf-8').splitlines():
      if line.strip():previous=json.loads(line)
    row={'schema_version':'1.0','run_id':self.folder.name,'seq':1 if previous is None else previous['seq']+1,'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'monotonic_ns':time.monotonic_ns(),'actor':self.actor,'cwd':redact(str(Path.cwd()),self.workspace),'phase':phase,'event_type':event_type,'previous_sha256':None if previous is None else previous['event_sha256'],**redact(data,self.workspace)}
    row['event_sha256']=hashlib.sha256(json.dumps(row,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    with self.path.open('ab') as f:f.write((json.dumps(row,ensure_ascii=False)+'\n').encode());f.flush();os.fsync(f.fileno())
    return row
   finally:
    if os.name=='nt':lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_UNLCK,1)
    else:fcntl.flock(lock,fcntl.LOCK_UN)
 def verify(self):
  previous=None;count=0
  if not self.path.exists():return {'events':0,'head_sha256':None,'scope':'empty local log'}
  for line in self.path.read_text(encoding='utf-8').splitlines():
   row=json.loads(line);digest=row.pop('event_sha256')
   if row['seq']!=count+1 or row['previous_sha256']!=previous or hashlib.sha256(json.dumps(row,sort_keys=True,separators=(',',':')).encode()).hexdigest()!=digest:raise ValueError('audit chain mismatch')
   previous=digest;count+=1
  return {'events':count,'head_sha256':previous,'scope':'local consistency only; not exhaustive or tamper-proof authenticity'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory',type=Path,required=True);p.add_argument('--run',required=True);p.add_argument('--event');p.add_argument('--phase',default='work');p.add_argument('--actor',default='agent');p.add_argument('--data',default='{}');p.add_argument('--verify',action='store_true');a=p.parse_args();r=Recorder(a.directory,a.run,a.actor,Path.cwd())
 if a.verify:print(json.dumps(r.verify()));return
 if not a.event:p.error('--event or --verify is required')
 if len(a.data)>65536:p.error('data is too large; log an artifact hash instead')
 data=json.loads(a.data)
 if not isinstance(data,dict):p.error('--data must be an object')
 print(json.dumps(r.append(a.event,a.phase,**data)))
if __name__=='__main__':main()
