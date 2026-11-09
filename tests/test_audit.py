import importlib.util,json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TEMP=ROOT/'artifacts/audit-tests';TEMP.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'skills/scenello/scripts'));sys.path.insert(0,str(ROOT/'evals/runner'))
import audit as log
from supervisor import supervise,safe_event,snapshot
class AuditTests(unittest.TestCase):
 def test_append_resume_chain(self):
  with tempfile.TemporaryDirectory(dir=TEMP) as d:
   a=log.Recorder(d,'test');a.append('start');b=log.Recorder(d,'test');b.append('resume');self.assertEqual(b.verify()['events'],2)
 def test_envelope_cannot_override(self):
  with tempfile.TemporaryDirectory(dir=TEMP) as d:
   with self.assertRaises(ValueError):log.Recorder(d,'test').append('bad',seq=99)
 def test_redaction_before_disk(self):
  with tempfile.TemporaryDirectory(dir=TEMP) as d:
   a=log.Recorder(d,'test');value='sk-'+'A'*40;a.append('safe',api_key=value,prompt='private input',prompt_sha256='abc',command='echo '+value)
   text=a.path.read_text();self.assertNotIn(value,text);self.assertNotIn('private input',text);self.assertEqual(json.loads(text)['prompt_sha256'],'abc')
 def test_detect_modified_history(self):
  with tempfile.TemporaryDirectory(dir=TEMP) as d:
   a=log.Recorder(d,'test');a.append('start');a.path.write_text(a.path.read_text().replace('start','changed'))
   with self.assertRaises(ValueError):a.verify()
 def test_no_raw_reasoning_or_messages(self):
  row=safe_event({'type':'item.completed','item':{'id':'1','type':'reasoning','text':'must not persist'}});self.assertNotIn('must not persist',json.dumps(row))
 def test_partial_stream_survives_timeout(self):
  with tempfile.TemporaryDirectory(dir=TEMP) as d:
   root=Path(d);project=root/'project';project.mkdir();command=[sys.executable,'-u','-c',"import json,time;print(json.dumps({'type':'thread.started','thread_id':'synthetic-test'}),flush=True);time.sleep(30)"]
   result=supervise(command,project,root/'output',timeout=5);self.assertEqual(result['status'],'timeout');self.assertEqual(result['event_count'],1);self.assertTrue((root/'output/agent-events.jsonl').read_text());self.assertEqual(result['outcome'],'INCOMPLETE')
 def test_starter_hash_tracks_actual_files(self):
  with tempfile.TemporaryDirectory(dir=TEMP) as d:
   root=Path(d);(root/'app.js').write_text('one');before=snapshot(root);(root/'app.js').write_text('two');self.assertNotEqual(before,snapshot(root))
 def test_nonzero_not_success(self):
  with tempfile.TemporaryDirectory(dir=TEMP) as d:
   root=Path(d);project=root/'project';project.mkdir();r=supervise([sys.executable,'-c','raise SystemExit(7)'],project,root/'out',timeout=3);self.assertEqual(r['status'],'agent_error');self.assertEqual(r['exit_code'],7);self.assertEqual(r['outcome'],'INCOMPLETE')

 def test_owned_child_cannot_survive_parent_exit(self):
  import time
  with tempfile.TemporaryDirectory(dir=TEMP) as d:
   root=Path(d);project=root/'project';project.mkdir();marker=root/'escaped'
   child="import time,pathlib;time.sleep(2);pathlib.Path("+repr(str(marker))+").write_text('escaped')"
   parent="import subprocess,sys;subprocess.Popen([sys.executable,'-c',"+repr(child)+"])"
   result=supervise([sys.executable,'-c',parent],project,root/'out',timeout=5)
   if sys.platform=='win32':self.assertEqual(result['child_supervision'],'windows-kill-on-close-job')
   time.sleep(2.2);self.assertFalse(marker.exists())

 def test_shell_payload_cannot_leak_private_prompt(self):
  secret='a confidential creative brief copied into a shell argument'
  row=safe_event({'type':'item.completed','item':{'type':'command_execution','command':'python -c '+secret,'exit_code':0}})
  self.assertNotIn(secret,json.dumps(row));self.assertIn('command_sha256',row['item'])

 def test_actual_cwd_is_recorded_and_not_overridable(self):
  with tempfile.TemporaryDirectory(dir=TEMP) as d:
   a=log.Recorder(d,'cwd',workspace=Path.cwd());self.assertEqual(a.append('measured')['cwd'],'<workspace>')
   with self.assertRaises(ValueError):a.append('invented',cwd='a fabricated location')
