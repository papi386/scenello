import importlib.util
import json
from pathlib import Path
import stat
import tempfile
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1]
TEMP=ROOT/"artifacts"/"unit-tmp"
TEMP.mkdir(parents=True,exist_ok=True)


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


intake=module("intake","skills/scenello/scripts/intake.py")
router=module("router","skills/scenello/scripts/route.py")
release=module("release","tools/release.py")


class IntakeTests(unittest.TestCase):
    def pack(self,entries,**limits):
        with tempfile.TemporaryDirectory(dir=TEMP) as d:
            f=Path(d)/"pack.zip"
            with zipfile.ZipFile(f,"w",zipfile.ZIP_DEFLATED) as z:
                for name,data in entries:z.writestr(name,data)
            return intake.inventory(f,**limits)

    def test_hash_not_execute(self):
        result=self.pack([("guide.md","hello"),("payload.py","raise RuntimeError('must never execute')")])
        self.assertEqual(result["entries"][0]["sha256"],"2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824")
        self.assertTrue(result["entries"][1]["executable_or_active"])
        self.assertEqual(result["entries"][1]["disposition"],"UNVERIFIED")

    def test_traversal_and_windows_aliases(self):
        for name in ("../out","/root","C:"+"/private","\\\\host\\share","NUL.txt","a:stream","x/./y","x. /z","x/../z"):
            with self.subTest(name=name):self.assertTrue(intake.path_risks(name)[1])

    def test_case_collision(self):
        r=self.pack([("A.md","a"),("a.md","b")])
        self.assertIn("duplicate-or-case-collision",r["entries"][1]["risks"])

    def test_file_directory_conflict(self):
        r=self.pack([("folder","file"),("folder/child.md","child")])
        self.assertTrue(all("file-directory-conflict" in e["risks"] for e in r["entries"]))

    def test_symlink(self):
        info=zipfile.ZipInfo("link");info.create_system=3;info.external_attr=(stat.S_IFLNK|0o777)<<16
        r=self.pack([(info,"target")]);self.assertIn("link-or-special-file",r["entries"][0]["risks"])

    def test_bomb_and_nested(self):
        r=self.pack([("huge.txt","0"*100000),("inner.zip","not expanded")],max_ratio=2)
        self.assertIn("expansion-ratio",r["entries"][0]["risks"])
        self.assertIn("nested-archive-not-expanded",r["entries"][1]["risks"])
        self.assertIsNone(r["entries"][0]["sha256"])

    def test_budget(self):
        with self.assertRaises(ValueError):self.pack([("a","12"),("b","34")],max_total=3)
        with self.assertRaises(ValueError):self.pack([("a","1"),("b","2")],max_entries=1)


class RoutingTests(unittest.TestCase):
    def test_routes_are_real(self):
        for query,target in [("diagonal cards shuffle","SCN-02"),("p99 latency frame","SCN-04"),("private zip facebook reference","SCN-05"),("blender 3d rig lighting","SCN-06")]:
            with self.subTest(query=query):self.assertIn(target,[e["id"] for e in router.route(query)["references"]])

    def test_negative_editing(self):
        self.assertEqual(router.route("Edit a reel soundtrack in ffmpeg")["scope"],"outside")

    def test_no_match(self):
        self.assertEqual(router.route("repair database migration")["scope"],"unresolved")


class ReleaseTests(unittest.TestCase):
    def test_secret_rules(self):
        self.assertIn("credential-token",release.findings("ghp_"+"a"*30))
        fake_path="/".join(["C:","Users","example","private"])
        fake_url="https"+"://"+"face"+"book"+".com"+"/private"
        self.assertIn("local-machine-path",release.findings(fake_path))
        self.assertIn("private-social-media-url",release.findings(fake_url))

    def test_active_svg_rejected(self):
        with self.assertRaises(ValueError):release.check_svg('<svg><script>alert(1)</script></svg>')
        with self.assertRaises(ValueError):release.check_svg('<svg onload="alert(1)"/>')

    def test_unknown_file_rejected(self):
        with tempfile.TemporaryDirectory(dir=TEMP) as d:
            r=Path(d);(r/"private.mov").write_bytes(b"private")
            with self.assertRaises(ValueError):release.files(r)

    def test_package_reproducible(self):
        with tempfile.TemporaryDirectory(dir=TEMP) as d:
            r=Path(d);(r/"README.md").write_text("original",encoding="utf-8")
            a=r/"one.zip";b=r/"two.zip"
            self.assertEqual(release.build(r,[r/"README.md"],a),release.build(r,[r/"README.md"],b))
            with self.assertRaises(ValueError):release.build(r,[r/"README.md"],a)

    def test_manifest_and_links(self):
        release.conformance(ROOT)


if __name__=="__main__":unittest.main()
