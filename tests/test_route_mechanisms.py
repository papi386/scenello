import importlib.util,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('scenello_route',Path(__file__).resolve().parents[1]/'skills/scenello/scripts/route.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class RouteMechanismTests(unittest.TestCase):
 def first(self,q):return mod.route(q)['references'][0]['id']
 def test_shared_image_architecture(self):self.assertEqual(self.first('Architectural website shared image to detail cinematic camera'),'SCN-02')
 def test_pbr_product(self):self.assertEqual(self.first('Lamp website studio lighting material and finish change'),'SCN-16')
 def test_journey(self):self.assertEqual(self.first('Immersive continuous camera travel through three worlds website'),'SCN-09')
 def test_festival(self):self.assertEqual(self.first('Festival program interface schedule filter website'),'SCN-21')
 def test_performance_priority(self):self.assertEqual(self.first('Website startup spike latency p99 mobile camera'),'SCN-04')
 def test_no_heavy_workflow_for_small_task(self):self.assertEqual(mod.route('animate cards on a web page')['workflow'],[])
 def test_editing_outside(self):self.assertEqual(mod.route('reel soundtrack montage')['scope'],'outside')

 def test_medium_hero_avoids_full_audit(self):self.assertEqual(mod.route('cinematic hero website')['workflow'],['art-direction.md','motion.md'])
 def test_large_site_loads_tools_and_validation(self):self.assertIn('skills-and-mcps.md',mod.route('full cinematic website')['workflow'])
