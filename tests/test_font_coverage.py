import importlib.util,unittest
from pathlib import Path
tool=Path(__file__).resolve().parents[1]/'tools/build_critical_fonts.py'
mod=None
if tool.exists():
 spec=importlib.util.spec_from_file_location('critical_fonts',tool);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
@unittest.skipIf(mod is None,"font build utility is source-only")
class CriticalFontCoverageTests(unittest.TestCase):
 def test_placeholder_is_not_stripped(self):self.assertIn(0x2026,mod.critical_codepoints('<textarea placeholder="Tell us…"></textarea>','index.html'))
 def test_encoded_attribute_is_kept(self):self.assertIn(0x2197,mod.critical_codepoints('<img alt="Go &#x2197;">','index.html'))
 def test_css_generated_content_is_kept(self):self.assertIn(0x2197,mod.critical_codepoints(r'.arrow::after{content:"\2197"}','style.css'))
