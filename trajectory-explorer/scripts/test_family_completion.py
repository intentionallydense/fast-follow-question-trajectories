"""Coverage and audit gate regressions for previously absent task families."""
import json, hashlib, unittest
from build_task_trajectories import ROOT, completion_data, COMPLETION

class FamilyCompletion(unittest.TestCase):
    def test_inventory_and_sparse_evidence(self):
        index=json.loads((ROOT/'app/tasks/audited-index.json').read_text())
        self.assertEqual(index['family_count'],41)
        self.assertEqual(len(index['tasks']),42)
        self.assertEqual(len({t['family_id'] for t in index['tasks']}),41)
        self.assertEqual(sum(t['account_count'] for t in index['tasks']),index['account_count'])
        for row in index['tasks']:
            data=json.loads((ROOT/'public'/row['file'].lstrip('/')).read_text())
            if not row['account_count']:
                self.assertEqual(data['coverage']['status'],'insufficient_evidence')
                self.assertTrue(data['coverage']['anchors'])
                self.assertEqual(data['rounds'],[])
            for c in (data.get('coverage') or {}).get('anchors',[]):
                self.assertEqual(c['body'][c['start_char']:c['end_char']],c['quote'])
                self.assertEqual(hashlib.sha256(c['quote'].encode('latin1')).hexdigest(),c['text_sha256'])

    def test_reviewed_additions_and_two_revision_threshold(self):
        dossiers=completion_data('dossiers.json')
        gate=json.loads((COMPLETION/'review-gate.json').read_text())
        self.assertEqual(gate['status'],'passed')
        self.assertEqual(set(gate['trajectory_ids']),{t['trajectory_id'] for t in dossiers})
        for t in dossiers:
            self.assertEqual(t['status'],'supported')
            self.assertGreaterEqual(len({m['revision_id'] for m in t['owned_messages']}),2)
            self.assertTrue(t['anchor_observation_ids'])
            for m in t['owned_messages']:
                self.assertTrue(m['rule_ids'])
                self.assertTrue(m['reason'])

if __name__=='__main__':unittest.main()
