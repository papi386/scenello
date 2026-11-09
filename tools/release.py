"""Offline privacy/conformance gate and deterministic allowlisted package builder.

No uploads, network, installs, Git staging or commits. Heuristic scan, not certification.
"""
import sys
sys.dont_write_bytecode=True
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = {".gitignore", ".gitattributes", "README.md", "LICENSE", "CONTRIBUTING.md", "SECURITY.md",
              "THIRD_PARTY_NOTICES.md", "plugin.json", "asset-manifest.json", "sbom.json"}
ROOT_DIRS = {"skills", "assets", "tools", "tests", "docs", "adapters", "evals", ".github"}
EXCLUDE = {".git", "artifacts", "dist", "__pycache__", ".agents", ".venv", "node_modules"}
EXTENSIONS = {".md", ".py", ".json", ".yaml", ".yml", ".svg", ".html", ".css", ".js", ".cjs", ".mjs", ".woff", ".txt"}
RULES = {
    "local-machine-path": re.compile(r"[A-Za-z]:[\\/](?:Users|dev)[\\/]|/(?:Users|home)/[\w.-]+/", re.I),
    "private-project-identifier": re.compile(r"omni(?:links)", re.I),
    "private-social-media-url": re.compile(r"https?://[^\s]*?(?:facebook\.com|fb\.watch|fbcdn\.net)/", re.I),
    "private-key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "credential-token": re.compile(r"\b(?:sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16})\b"),
    "assigned-secret": re.compile(r'''(?im)(?:api_key|access_token|password)\s*[:=]\s*["'][^"']{8,}["']'''),
}


def findings(text):
    return [label for label, pattern in RULES.items() if pattern.search(text)]


def files(root, consumer=False):
    root = root.resolve()
    result = []
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        if consumer and rel.as_posix()=="release-checksums.json":
            continue
        if any(part in EXCLUDE for part in rel.parts):
            continue
        if p.is_symlink():
            raise ValueError(f"symlink forbidden: {rel.as_posix()}")
        if p.is_dir():
            continue
        if not p.resolve().is_relative_to(root):
            raise ValueError("path escaped repository")
        if (len(rel.parts) == 1 and rel.name not in ROOT_FILES) or (len(rel.parts)>1 and rel.parts[0] not in ROOT_DIRS):
            raise ValueError(f"unreviewed root: {rel.as_posix()}")
        if rel.name not in ROOT_FILES and p.suffix not in EXTENSIONS:
            raise ValueError(f"unreviewed extension: {rel.as_posix()}")
        if p.stat().st_size > 2*1024**2:
            raise ValueError(f"member exceeds project release limit: {rel.as_posix()}")
        result.append(p)
    if sum(p.stat().st_size for p in result)>8*1024**2:
        raise ValueError("package exceeds project 8 MiB content budget")
    return result


def check_svg(text):
    if "<!" in text:
        raise ValueError("SVG declaration/entity forbidden")
    tree = ET.fromstring(text)
    for e in tree.iter():
        if e.tag.split("}")[-1] in ("script", "foreignObject", "image", "use"):
            raise ValueError("SVG active/external element forbidden")
        for k, v in e.attrib.items():
            if k.lower().startswith("on") or "href" in k or "url(http" in v.lower():
                raise ValueError("SVG event/external reference forbidden")


def conformance(root):
    # Authored checks against selected current manifest constraints. Not an official validator.
    m = json.loads((root/"plugin.json").read_text(encoding="utf-8"))
    if m.get("$schema")!="https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        raise ValueError("unknown portable manifest schema")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", m.get("name", "")):
        raise ValueError("invalid package name")
    if set(m)-{"$schema","name","version","description","author","homepage","repository","license","keywords","extensions"}:
        raise ValueError("unknown portable manifest field")
    ui=m["extensions"]["com.openai"]["interface"]
    for k, limit in {"displayName":30,"shortDescription":30,"longDescription":4000,"developerName":80}.items():
        if not isinstance(ui.get(k), str) or not 0<len(ui[k])<=limit:
            raise ValueError(f"invalid interface {k}")
    for k in ("composerIcon","logo"):
        path=ui[k]
        if not path.startswith("./") or ".." in Path(path).parts:
            raise ValueError("unsafe icon path")
        asset=(root/path).resolve()
        if not asset.is_relative_to(root.resolve()) or not asset.is_file():
            raise ValueError("missing icon")
        icon=ET.fromstring(asset.read_text(encoding="utf-8"))
        box=[float(x) for x in icon.attrib["viewBox"].split()]
        if box[2]!=box[3] or box[2]<48:
            raise ValueError("icon must be square and >=48")
    skill=root/"skills/scenello/SKILL.md"
    text=skill.read_text(encoding="utf-8")
    head=text.split("---",2)[1]
    fields=dict(re.findall(r"^(\w+): (.+)$",head,re.M))
    if fields.get("name")!="scenello" or not 0<len(fields.get("description",""))<=1024:
        raise ValueError("invalid skill metadata")
    for target in re.findall(r"\]\(([^)]+)\)", text):
        if "://" not in target and not (skill.parent/target).is_file():
            raise ValueError("broken skill reference: "+target)
    for guide in [skill, *sorted((skill.parent/"references").rglob("*.md"))]:
        for target in re.findall(r"\]\(([^)]+)\)", guide.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            target=target.split("#",1)[0]
            if target and not (guide.parent/target).exists():
                raise ValueError("broken guide reference: "+str(guide.relative_to(root))+" -> "+target)
    if m["extensions"]["com.openai"].get("requires_local_executor") is not True:
        raise ValueError("local website implementation requires executor metadata")
    for e in json.loads((skill.parent/"references/techniques.json").read_text(encoding="utf-8")):
        if not (skill.parent/"references"/e["module"]).is_file() or not (skill.parent/e["demo"]).exists():
            raise ValueError("broken technique mapping: "+e["id"])
    manifest=root/"asset-manifest.json"
    if manifest.exists():
        for asset in json.loads(manifest.read_text(encoding="utf-8"))["assets"]:
            p=(root/asset["file"]).resolve(strict=True)
            if not p.is_relative_to(root.resolve()):
                raise ValueError("asset manifest escaped package")
            data=p.read_bytes()
            if len(data)!=asset["bytes"] or hashlib.sha256(data).hexdigest()!=asset["sha256"]:
                raise ValueError("stale asset provenance: "+asset["file"])


def history_check(root):
    rev=subprocess.run(["git","rev-list","--all"],cwd=root,capture_output=True,text=True,check=True)
    revisions=rev.stdout.splitlines()
    for revision in revisions:
        listing=subprocess.run(["git","ls-tree","-r","--name-only",revision],cwd=root,capture_output=True,text=True,check=True).stdout.splitlines()
        for name in listing:
            if findings(name) or name.endswith((".mp4",".mov",".wav",".env",".blend")):
                raise ValueError("history contains sensitive or excluded path")
            content=subprocess.run(["git","show",f"{revision}:{name}"],cwd=root,capture_output=True,check=True).stdout
            if len(content)>2*1024**2 or findings(content.decode("utf-8",errors="replace")):
                raise ValueError("history contains excluded content")
    return len(revisions)


def scan(root, consumer=False):
    paths=files(root,consumer)
    errors=[]
    for path in paths:
        rel=path.relative_to(root).as_posix()
        if path.suffix==".woff":
            if path.parent!=root/"skills/scenello/assets/examples/fonts" or not path.read_bytes().startswith(b"wOFF") or path.stat().st_size>65536:
                raise ValueError("unreviewed font binary: "+rel)
            manifest=json.loads((root/"asset-manifest.json").read_text(encoding="utf-8"))
            listed=next((a for a in manifest["assets"] if a["file"]==rel),None)
            if not listed or listed["license"]!="OFL-1.1" or not (path.parent/"LICENSE.txt").exists():
                raise ValueError("missing reviewed font rights: "+rel)
            continue
        text=path.read_text(encoding="utf-8")
        hits=findings(rel+"\n"+text)
        if hits:
            errors.append({"file":rel,"rules":hits})
        if path.suffix==".svg":
            check_svg(text)
    if errors:
        raise ValueError(json.dumps(errors))
    conformance(root)
    return paths


PUBLIC_DOCS = {"install.md", "readiness.md", "release.md", "prompts.md", "privacy.md", "changelog.md", "agent-compatibility.md", "release-validation.md"}
PUBLIC_TOOLS = {"install.py", "release.py", "verify_package.py"}

def public_files(root, paths):
    """Select the reviewed beta payload after scanning every source file."""
    selected=[]
    for p in paths:
        rel=p.relative_to(root).as_posix()
        if rel.startswith("docs/") and rel.split("/",1)[1] not in PUBLIC_DOCS:continue
        if rel.startswith("tools/") and rel.split("/",1)[1] not in PUBLIC_TOOLS:continue
        if rel.startswith("evals/") and not rel.startswith("evals/runner/"):continue
        if rel.startswith("adapters/"):continue
        selected.append(p)
    return selected

def build(root, paths, output):
    if output.exists():
        raise ValueError("refusing to overwrite package; choose a new path")
    output.parent.mkdir(parents=True,exist_ok=True)
    snapshot={p.relative_to(root).as_posix():p.read_bytes() for p in paths}
    hashes={name:hashlib.sha256(data).hexdigest() for name,data in snapshot.items()}
    with zipfile.ZipFile(output,"x",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in snapshot.items():
            entry=zipfile.ZipInfo(name,(2026,1,1,0,0,0))
            entry.external_attr=0o100644<<16;entry.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(entry,data)
        entry=zipfile.ZipInfo("release-checksums.json",(2026,1,1,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(entry,json.dumps(hashes,indent=2))
    return hashlib.sha256(output.read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--package",type=Path)
    args=p.parse_args()
    if (ROOT/"release-checksums.json").exists():
        if args.package:p.error("build from a source checkout; use verify_package.py for downloaded packages")
        from verify_package import verify_directory
        print(json.dumps(verify_directory(ROOT),indent=2));return
    paths=scan(ROOT)
    revisions=history_check(ROOT)
    report={"files":len(paths),"content_bytes":sum(p.stat().st_size for p in paths),"history_revisions":revisions,"version":json.loads((ROOT/"plugin.json").read_text())["version"],"scan":"PASS (heuristic)","conformance":"authored structural checks, not official approval"}
    recovery=ROOT/"docs/recovery-status.json"
    if recovery.exists():
        gate=json.loads(recovery.read_text(encoding="utf-8"));report["recovery_release_status"]=gate["release_status"]
        if args.package and gate["release_status"]=="BLOCKED":
            raise ValueError("Packaging blocked by recorded recovery gates. Read docs/recovery-status.json; scans are not artistic approval.")
    if args.package:
        report["package_sha256"]=build(ROOT,public_files(ROOT,paths),args.package.resolve())
        report["package_bytes"]=args.package.stat().st_size
    print(json.dumps(report,indent=2))


if __name__=="__main__":
    main()
