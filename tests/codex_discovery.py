"""Exercise actual Codex app-server discovery in a new isolated local project.

No model turn, account sign-in, remote publication or global configuration change.
Requires existing Codex CLI. Output is under ignored artifacts/.
"""
import importlib.util
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import threading
import time
import uuid

ROOT=Path(__file__).resolve().parents[1]


def main():
    cli=shutil.which("codex")
    if not cli:
        raise SystemExit("Codex CLI unavailable; discovery untested")
    fixture=ROOT/"artifacts"/("codex-discovery-"+uuid.uuid4().hex[:8])
    fixture.mkdir(parents=True,exist_ok=True)
    subprocess.run(["git","init","-b","test/scenello-discovery",str(fixture)],check=True,capture_output=True)
    spec=importlib.util.spec_from_file_location("installer",ROOT/"tools/install.py")
    installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)
    target=fixture/".agents/skills/scenello"
    if not target.exists():installer.install(fixture,apply=True)
    # Isolate all CLI state; never copy a real auth/config file into the fixture.
    cli_home=fixture/"isolated-cli-home";cli_home.mkdir(exist_ok=True)
    env=os.environ.copy();env["CODEX_HOME"]=str(cli_home)
    messages=queue.Queue()
    with (fixture/"stderr.log").open("w",encoding="utf-8") as errors:
        process=subprocess.Popen([cli,"app-server"],cwd=fixture,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=errors,text=True,encoding="utf-8")
        def read():
            for line in process.stdout:
                try:messages.put(json.loads(line))
                except json.JSONDecodeError:pass
        threading.Thread(target=read,daemon=True).start()
        def send(message):
            process.stdin.write(json.dumps(message)+"\n");process.stdin.flush()
        def response(ident):
            deadline=time.monotonic()+25
            while time.monotonic()<deadline:
                try:message=messages.get(timeout=.5)
                except queue.Empty:continue
                if message.get("id")==ident:return message
            raise TimeoutError("Codex response timeout")
        try:
            send({"id":0,"method":"initialize","params":{"clientInfo":{"name":"scenello_local_test","version":"0.1.0"}}})
            initialized=response(0)
            if "error" in initialized:raise RuntimeError(initialized["error"])
            send({"method":"initialized"})
            send({"id":1,"method":"skills/list","params":{"cwds":[str(fixture)],"forceReload":True}})
            result=response(1)
            (fixture/"private-discovery-response.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
            if "error" in result:raise RuntimeError(result["error"])
            rows=result["result"]["data"]
            matches=[s for row in rows for s in row.get("skills",[]) if s["name"]=="scenello"]
            assert len(matches)==1, "canonical skill not discovered exactly once"
            assert matches[0].get("enabled",True), "skill is disabled"
            report={"discovery":"PASS","name":matches[0]["name"],"enabled":matches[0].get("enabled"),"interface":matches[0].get("interface"),"parse_errors":sum(len(row.get("errors",[])) for row in rows),"model_activation":"not exercised","cli_version":subprocess.run([cli,"--version"],capture_output=True,text=True).stdout.strip()}
            (ROOT/"artifacts/codex-discovery-summary.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
            print(json.dumps(report))
        finally:
            process.stdin.close()
            try:process.wait(timeout=5)
            except subprocess.TimeoutExpired:process.terminate();process.wait(timeout=5)


if __name__=="__main__":main()
