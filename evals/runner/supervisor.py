"""Streaming, privacy-filtered agent process supervision. No automatic auth or permission changes."""
import hashlib,json,os,signal,subprocess,sys,threading,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'skills/scenello/scripts'))
from audit import Recorder,redact

def snapshot(folder):
 result={}
 for p in sorted(Path(folder).rglob('*')):
  if p.is_file() and not p.is_symlink() and not any(x in ('.git','node_modules','__pycache__') for x in p.relative_to(folder).parts):result[p.relative_to(folder).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
 return result

def safe_event(event):
 """Keep event schema/operation evidence, not user messages or model reasoning."""
 if not isinstance(event,dict):return {'type':'unsupported_event','value_sha256':hashlib.sha256(json.dumps(event).encode()).hexdigest()}
 kept={k:event[k] for k in ('type','thread_id','turn_id','status','model') if k in event}
 item=event.get('item')
 if isinstance(item,dict):
  kept['item']={k:item[k] for k in ('id','type','status','exit_code','tool','server') if k in item}
  if 'command' in item:
   command=str(item['command']);kept['item']['command_sha256']=hashlib.sha256(command.encode()).hexdigest();kept['item']['command_lines']=len(command.splitlines());kept['item']['mentions_canonical_skill']='scenello/SKILL.md' in command.replace('\\','/')
   kept['item']['command_policy']='Digest-only shell payload: may contain confidential inline prompts. File changes/status retained; canonical-skill mention alone is not proof of a successful read.'
  if 'aggregated_output' in item:kept['item']['output_sha256']=hashlib.sha256(str(item['aggregated_output']).encode()).hexdigest()
  if isinstance(item.get('changes'),list):kept['item']['changes']=[{k:c[k] for k in ('path','kind') if k in c} for c in item['changes'] if isinstance(c,dict)]
 if event.get('type') in ('error','turn.failed'):
  # Do not indiscriminately preserve arbitrary provider payloads or raw prompts.
  kept['error_present']=True;kept['error_sha256']=hashlib.sha256(json.dumps(event,sort_keys=True).encode()).hexdigest()
 return kept


class ChildGroup:
 """Own only this supervised process tree; no system-wide process enumeration."""
 def __init__(self, process):
  self.process=process;self.handle=None;self.mode='posix-session' if os.name!='nt' else 'best-effort'
  if os.name=='nt':
   import ctypes
   from ctypes import wintypes as w
   class Basic(ctypes.Structure):
    _fields_=[('ProcessTime',ctypes.c_int64),('JobTime',ctypes.c_int64),('Flags',w.DWORD),('Minimum',ctypes.c_size_t),('Maximum',ctypes.c_size_t),('Active',w.DWORD),('Affinity',ctypes.c_size_t),('Priority',w.DWORD),('Scheduling',w.DWORD)]
   class IO(ctypes.Structure):
    _fields_=[(n,ctypes.c_uint64) for n in ('ReadOps','WriteOps','OtherOps','ReadBytes','WriteBytes','OtherBytes')]
   class Extended(ctypes.Structure):
    _fields_=[('Basic',Basic),('IO',IO),('ProcessMemory',ctypes.c_size_t),('JobMemory',ctypes.c_size_t),('PeakProcess',ctypes.c_size_t),('PeakJob',ctypes.c_size_t)]
   self.kernel=ctypes.WinDLL('kernel32',use_last_error=True)
   self.kernel.CreateJobObjectW.argtypes=[ctypes.c_void_p,w.LPCWSTR];self.kernel.CreateJobObjectW.restype=w.HANDLE
   self.kernel.SetInformationJobObject.argtypes=[w.HANDLE,ctypes.c_int,ctypes.c_void_p,w.DWORD]
   self.kernel.AssignProcessToJobObject.argtypes=[w.HANDLE,w.HANDLE];self.kernel.CloseHandle.argtypes=[w.HANDLE]
   handle=self.kernel.CreateJobObjectW(None,None);limits=Extended();limits.Basic.Flags=0x2000
   if handle and self.kernel.SetInformationJobObject(handle,9,ctypes.byref(limits),ctypes.sizeof(limits)) and self.kernel.AssignProcessToJobObject(handle,int(process._handle)):
    self.handle=handle;self.mode='windows-kill-on-close-job'
   elif handle:self.kernel.CloseHandle(handle)
 def close(self):
  if self.handle:self.kernel.CloseHandle(self.handle);self.handle=None
  elif os.name!='nt':
   try:os.killpg(self.process.pid,signal.SIGKILL)
   except ProcessLookupError:pass


def supervise(command,project,output,timeout=600,input_bytes=None,env=None):
 project=Path(project).resolve();output=Path(output).resolve();output.mkdir(parents=True,exist_ok=False)
 recorder=Recorder(output,'audit',workspace=project);before=snapshot(project);record={'command':command,'starting_files':before,'starting_state_sha256':hashlib.sha256(json.dumps(before,sort_keys=True).encode()).hexdigest(),'requested_timeout_s':timeout,'outcome':'INCOMPLETE','activation':'UNKNOWN','isolation':'Caller must separately verify global/project skill and auth boundaries'}
 recorder.append('process_start','execution',operation=command,starting_state_sha256=record['starting_state_sha256']);started=time.monotonic();failed_event=False;thread_id=None;status='running';count=0;launch_error=None
 flags={'creationflags':subprocess.CREATE_NEW_PROCESS_GROUP} if os.name=='nt' else {'start_new_session':True}
 child_env=dict(os.environ if env is None else env);child_env.setdefault('CHROME_LOG_FILE',str(output/'browser-diagnostics.log'))
 try:process=subprocess.Popen(command,cwd=project,env=child_env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,**flags)
 except OSError as e:
  recorder.append('launch_failed','execution',status='failed',error=str(e));record.update(status='launch_error',exit_code=None,final_files=snapshot(project));(output/'result.json').write_text(json.dumps(record,indent=2),encoding='utf-8');return record
 group=ChildGroup(process);record['child_supervision']=group.mode;diagnostic_flags=set()
 recorder.append('child_group_created','execution',mode=group.mode,status='observed')
 def read_stdout():
  nonlocal failed_event,thread_id,count
  with (output/'agent-events.jsonl').open('ab') as f:
   for raw in process.stdout:
    try:event=json.loads(raw)
    except (json.JSONDecodeError,UnicodeDecodeError):
     recorder.append('non_json_output','execution',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest());continue
    safe=redact(safe_event(event),project);count+=1
    if safe.get('thread_id'):thread_id=safe['thread_id']
    if safe.get('type') in ('turn.failed','error'):failed_event=True
    f.write((json.dumps(safe)+'\n').encode());f.flush();os.fsync(f.fileno());recorder.append('agent_event','execution',event=safe,status='failed' if safe.get('type') in ('turn.failed','error') else 'observed')
 def read_stderr():
  with (output/'diagnostics.log').open('a',encoding='utf-8') as f:
   for raw in process.stderr:
    # CLI diagnostics only, bounded/redacted; never save a raw transcript.
    text=redact(raw.decode('utf-8',errors='replace'),project)[:4000]
    if '401 Unauthorized' in text and 'Missing bearer or basic authentication' in text:diagnostic_flags.add('authentication-unavailable')
    f.write(text);f.flush()
 def feed_stdin():
  try:
   if input_bytes:process.stdin.write(input_bytes)
   process.stdin.close()
  except (BrokenPipeError,OSError):recorder.append('stdin_closed_early','execution',status='observed')
 threads=[threading.Thread(target=read_stdout,daemon=True),threading.Thread(target=read_stderr,daemon=True),threading.Thread(target=feed_stdin,daemon=True)]
 for t in threads:t.start()
 try:
  code=process.wait(timeout=timeout);status='agent_error' if code or failed_event else 'exited'
 except (subprocess.TimeoutExpired,KeyboardInterrupt):
  status='timeout' if time.monotonic()-started>=timeout else 'interrupted';recorder.append('termination_requested','execution',status=status,pid=process.pid)
  if process.poll() is None:
   try:
    if os.name=='nt':process.send_signal(signal.CTRL_BREAK_EVENT)
    else:os.killpg(process.pid,signal.SIGTERM)
    code=process.wait(timeout=3)
   except (OSError,subprocess.TimeoutExpired):
    if os.name=='nt' and process.poll() is None:subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],capture_output=True)
    elif os.name!='nt':
     try:os.killpg(process.pid,signal.SIGKILL)
     except ProcessLookupError:pass
    if process.poll() is None:process.kill()
    code=process.wait()
  else:code=process.returncode
 finally:
  group.close()
  for t in threads:t.join(timeout=3)
  for pipe in (process.stdin,process.stdout,process.stderr):
   if pipe and not pipe.closed:pipe.close()
 after=snapshot(project);record['failure_classification']=sorted(diagnostic_flags) or ([status] if status!='exited' else []);record.update(status=status,exit_code=code,event_count=count,session_id=thread_id,duration_s=round(time.monotonic()-started,3),final_files=after,changed_files=[name for name in sorted(before.keys()|after.keys()) if before.get(name)!=after.get(name)],resume='Use supported codex exec resume only after verifying recorded session and isolation; no automatic replay',validation='Exit status is not creative/functional acceptance')
 recorder.append('process_finished','execution',status=status,exit_code=code,event_count=count,session_id=thread_id,changed_files=record['changed_files']);record['audit']=recorder.verify();(output/'result.json').write_text(json.dumps(redact(record,project),indent=2),encoding='utf-8');return record
