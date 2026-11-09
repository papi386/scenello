"""Offline consumer verification. Checks integrity/safety; no Git, installation or execution.
Checksums establish consistency, not publisher authenticity; compare a trusted external SHA-256.
"""
import sys
sys.dont_write_bytecode=True
import argparse,hashlib,json,stat,tempfile,zipfile
from pathlib import Path,PurePosixPath
import release
MANIFEST='release-checksums.json'
def safe(name):
 p=PurePosixPath(name)
 if not name or '\\' in name or p.is_absolute() or any(x in ('','..','.') for x in name.split('/')) or ':' in name or any(x.rstrip(' .')!=x for x in p.parts):raise ValueError('unsafe package path')
 if any(x.split('.')[0].upper() in {'CON','PRN','AUX','NUL',*[f'COM{i}' for i in range(1,10)],*[f'LPT{i}' for i in range(1,10)]} for x in p.parts):raise ValueError('reserved package path')
 return name

def verify_directory(root):
 root=Path(root).resolve();mp=root/MANIFEST
 if not mp.is_file() or mp.is_symlink() or mp.stat().st_size>131072:raise ValueError('missing/oversized integrity manifest')
 def unique(pairs):
  d={}
  for k,v in pairs:
   if k in d:raise ValueError('duplicate manifest key')
   d[k]=v
  return d
 manifest=json.loads(mp.read_text(encoding='utf-8'),object_pairs_hook=unique)
 if not isinstance(manifest,dict) or not manifest:raise ValueError('invalid integrity manifest')
 seen=set();total=0
 for name,sha in manifest.items():
  safe(name)
  if name==MANIFEST or name.casefold() in seen or not isinstance(sha,str) or len(sha)!=64:raise ValueError('invalid manifest member')
  seen.add(name.casefold());p=root/name
  if any(q.is_symlink() for q in (p,*p.parents) if q!=root.parent) or not p.resolve().is_relative_to(root) or not p.is_file():raise ValueError('missing or symlinked member')
  if p.stat().st_size>2*1024**2:raise ValueError('oversized member')
  raw=p.read_bytes();total+=len(raw)
  if total>8*1024**2:raise ValueError('oversized package')
  if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('checksum mismatch: '+name)
 actual=set()
 for p in root.rglob('*'):
  if p.is_symlink():raise ValueError('symlink forbidden')
  if p.is_file():actual.add(p.relative_to(root).as_posix())
 if actual!=set(manifest)|{MANIFEST}:raise ValueError('unexpected or missing files')
 # The source scanner still enforces every root/extension/provenance rule.
 paths=release.scan(root,consumer=True)
 if {p.relative_to(root).as_posix() for p in paths}!=set(manifest):raise ValueError('payload mismatch')
 return {'verification':'PASS','files':len(manifest),'bytes':total,'git_required':False,'authenticity':'compare trusted external archive hash'}

def verify_zip(path,temp_dir=None):
 with tempfile.TemporaryDirectory(prefix='scenello-verify-',dir=temp_dir) as directory:
  root=Path(directory);names=set();total=0
  with zipfile.ZipFile(path) as z:
   if len(z.infolist())>1000:raise ValueError('too many members')
   for info in z.infolist():
    name=safe(info.filename)
    if name.casefold() in names:raise ValueError('duplicate archive path')
    names.add(name.casefold());mode=info.external_attr>>16
    if info.is_dir() or stat.S_ISLNK(mode) or (stat.S_IFMT(mode) not in (0,stat.S_IFREG)):raise ValueError('nonregular archive member')
    total+=info.file_size
    if info.file_size>2*1024**2 or total>8*1024**2+131072:raise ValueError('oversized archive')
   for info in z.infolist():
    p=root/info.filename;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(info))
  return verify_directory(root)

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('package',type=Path);p.add_argument('--temp-dir',type=Path);a=p.parse_args()
 try:print(json.dumps(verify_directory(a.package) if a.package.is_dir() else verify_zip(a.package,a.temp_dir or a.package.resolve().parent)))
 except (ValueError,OSError,KeyError,IndexError,TypeError,zipfile.BadZipFile) as e:p.exit(1,'Verification failed: '+str(e)+'\n')
if __name__=='__main__':main()
