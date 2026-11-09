import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("install",ROOT/"tools/install.py")
installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)
TEMP=ROOT/"artifacts"/"unit-tmp";TEMP.mkdir(parents=True,exist_ok=True)


class InstallTests(unittest.TestCase):
    def test_dry_run_then_copy(self):
        with tempfile.TemporaryDirectory(dir=TEMP) as d:
            sentinel=Path(d)/"project.txt";sentinel.write_text("keep")
            path=installer.install(d)
            self.assertFalse(path.exists())
            installer.install(d,apply=True)
            self.assertTrue((path/"SKILL.md").is_file())
            self.assertTrue((path/"LICENSE").is_file())
            self.assertTrue((path/"assets/examples/materials/index.html").is_file())
            self.assertEqual((path/"SKILL.md").read_bytes(),(installer.SOURCE/"SKILL.md").read_bytes())
            with self.assertRaises(ValueError):installer.install(d,apply=True)
            self.assertEqual(sentinel.read_text(),"keep")

    def test_missing_project(self):
        with tempfile.TemporaryDirectory(dir=TEMP) as d:
            with self.assertRaises(FileNotFoundError):installer.install(Path(d)/"missing")


if __name__=="__main__":unittest.main()
