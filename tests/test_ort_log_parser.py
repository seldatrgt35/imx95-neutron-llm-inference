import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from analyze_neutron_ort_log import analyze

class TestPlacement(unittest.TestCase):
    def test_parser_does_not_confuse_static_assignment_with_execution(self):
        log='''
2026 [V:onnxruntime:, session_state.cc:1313 VerifyEachNodeIsAssignedToAnEp] Node(s) placed on [NeutronExecutionProvider]. Number of nodes: 2
2026 [V:onnxruntime:, session_state.cc:1315 VerifyEachNodeIsAssignedToAnEp]   MatMulNBits (/foo)
2026 [V:onnxruntime:, session_state.cc:1315 VerifyEachNodeIsAssignedToAnEp]   MatMulNBits (/bar)
2026 [V:onnxruntime:, session_state.cc:1313 VerifyEachNodeIsAssignedToAnEp] Node(s) placed on [CPUExecutionProvider]. Number of nodes: 1
2026 [V:onnxruntime:, session_state.cc:1315 VerifyEachNodeIsAssignedToAnEp]   Add (/baz)
'''
        r=analyze(log)
        self.assertEqual(r['session_setup_node_placements']['NeutronExecutionProvider'],2)
        self.assertEqual(r['operator_details']['NeutronExecutionProvider']['MatMulNBits'],2)
        self.assertEqual(r['operator_details']['CPUExecutionProvider']['Add'],1)
        self.assertEqual(r['status'],'STATIC_ASSIGNMENT_ONLY')

if __name__=='__main__':unittest.main()
