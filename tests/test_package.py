import unittest,sys,tempfile,zipfile,json,hashlib,stat
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import release,verify_package as v
ROOT=Path(__file__).resolve().parents[1]
class PackageTests(unittest.TestCase):
 def setUp(self):
  scratch=ROOT/"artifacts";scratch.mkdir(exist_ok=True)
  self.tmp=tempfile.TemporaryDirectory(dir=scratch);self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  manifest=ROOT/'release-checksums.json'
  if manifest.exists():
   entries=json.loads(manifest.read_text())
   for name,digest in entries.items():self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),digest)
   members=[ROOT/name for name in entries]
  else:members=release.public_files(ROOT,release.scan(ROOT))
  self.archive=self.root/'good.zip';release.build(ROOT,members,self.archive)
 def altered(self,change,update=False):
  with zipfile.ZipFile(self.archive) as z:d={n:z.read(n) for n in z.namelist()}
  change(d)
  if update:d['release-checksums.json']=json.dumps({n:hashlib.sha256(raw).hexdigest() for n,raw in d.items() if n!='release-checksums.json'}).encode()
  p=self.root/'bad.zip'
  with zipfile.ZipFile(p,'w') as z:
   for n,raw in d.items():z.writestr(n,raw)
  with self.assertRaises((ValueError,KeyError,IndexError)):v.verify_zip(p,self.root)
 def test_valid_zip_and_extracted_without_git(self):
  self.assertEqual(v.verify_zip(self.archive,self.root)['verification'],'PASS')
  target=self.root/'extracted';target.mkdir()
  with zipfile.ZipFile(self.archive) as z:z.extractall(target)
  self.assertEqual(v.verify_directory(target)['git_required'],False)
 def test_modified(self):self.altered(lambda d:d.update({'README.md':b'changed'}))
 def test_missing(self):self.altered(lambda d:d.pop('README.md'))
 def test_added(self):self.altered(lambda d:d.update({'unexpected.txt':b'extra'}),True)
 def test_traversal(self):self.altered(lambda d:d.update({'../escape':b'extra'}),True)
 def test_oversized(self):self.altered(lambda d:d.update({'docs/big.txt':b'x'*(2*1024**2+1)}),True)
 def test_checksum(self):self.altered(lambda d:d.update({'release-checksums.json':b'{"README.md":"bad"}'}))
 def test_frontmatter(self):self.altered(lambda d:d.update({'skills/scenello/SKILL.md':b'invalid'}),True)
 def test_reference(self):self.altered(lambda d:d.update({'skills/scenello/SKILL.md':d['skills/scenello/SKILL.md']+b'\n[broken](missing.md)'}),True)
 def test_plugin(self):self.altered(lambda d:d.update({'plugin.json':b'{}'}),True)
 def test_binary(self):self.altered(lambda d:d.update({'assets/foreign.exe':b'MZpayload'}),True)
 def test_svg(self):self.altered(lambda d:d.update({'assets/evil.svg':b'<svg><script>bad()</script></svg>'}),True)
 def test_duplicate(self):
  with zipfile.ZipFile(self.archive,'a') as z:z.writestr('README.md',b'duplicate')
  with self.assertRaises(ValueError):v.verify_zip(self.archive,self.root)
 def test_symlink(self):
  with zipfile.ZipFile(self.archive,'a') as z:
   i=zipfile.ZipInfo('assets/link');i.create_system=3;i.external_attr=(stat.S_IFLNK|0o777)<<16;z.writestr(i,'../README.md')
  with self.assertRaises(ValueError):v.verify_zip(self.archive,self.root)
