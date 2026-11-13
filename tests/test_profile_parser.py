import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from analyze_ort_profile import analyze_events

class TestProfile(unittest.TestCase):
    def test_profile(self):
        data=[{'name':'MatMul_0_kernel_time','cat':'Node','dur':42,'args':{'provider':'CPUExecutionProvider'}},
              {'name':'unrelated','dur':10,'args':{}},
              {'name':'Q4_0_kernel_time','cat':'Node','dur':15,'args':{'provider':'NeutronExecutionProvider'}}]
        r=analyze_events(data)
        self.assertEqual(r['provider_kernel_events']['CPUExecutionProvider'],1)
        self.assertEqual(r['provider_kernel_events']['NeutronExecutionProvider'],1)
        self.assertEqual(r['provider_event_duration_us']['NeutronExecutionProvider'],15)
if __name__=='__main__':unittest.main()
