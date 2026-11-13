import json
import hashlib
from pathlib import Path
import unittest

class TestEvidence(unittest.TestCase):
    def test_manifest(self):
        r=Path(__file__).resolve().parents[1]
        m=json.loads((r/'evidence/manifest.json').read_text())
        self.assertGreaterEqual(len(m['records']),10)
        for e in m['records']:
            f=e['public_evidence']
            if not f:continue
            payload=(r/f).read_bytes()
            self.assertEqual(hashlib.sha256(payload).hexdigest(),e['public_evidence_sha256'])
if __name__=='__main__':unittest.main()
