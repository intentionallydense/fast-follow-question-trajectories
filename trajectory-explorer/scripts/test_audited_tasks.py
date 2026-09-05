"""Regression checks for supported membership and source-owned matrix cells."""
import hashlib
import json
import unittest
from build_task_trajectories import ROOT

class AuditedTasks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index=json.loads((ROOT/'app/tasks/audited-index.json').read_text())
        cls.tasks=[json.loads((ROOT/'public'/t['file'].lstrip('/')).read_text()) for t in cls.index['tasks']]
        cls.accounts={a['id']:a for t in cls.tasks for a in t['accounts']}

    def test_supported_membership_is_not_legacy_accounts(self):
        roster=json.loads((ROOT/'app/tasks/assembled-index.json').read_text())['trajectories']
        self.assertEqual(set(self.accounts),{r['id'] for r in roster if r['status']!='provisional'})
        self.assertNotIn('P43',self.accounts)
        self.assertEqual(self.index['account_count'],len(self.accounts))
        self.assertEqual(sum(len(t['accounts']) for t in self.tasks),len(self.accounts))
        self.assertNotIn('labor-force-followup',{t['id'] for t in self.tasks})
        self.assertEqual(next(t['id'] for t in self.tasks if any(a['id']=='C556a612bd1ee/1' for a in t['accounts'])), 'ihme-lymphatic-filariasis')
        for file in ['tasks.tsx','../legacy-tasks/page.tsx']:
            source=(ROOT/'app/tasks'/file).read_text()
            if file=='tasks.tsx':
                self.assertNotIn("from './reconstruction.json'",source)
                self.assertNotIn("from './environments.json'",source)

    def test_every_event_and_timing_uses_owned_source(self):
        for a in self.accounts.values():
            dossier=json.loads((ROOT/'public'/a['dossier_file'].lstrip('/')).read_text())
            for claim in a['events']+a['timing']:
                c=claim['citation']
                with self.subTest(account=a['id'],revision=c['revision_id']):
                    self.assertTrue(any(m['revision_id']==c['revision_id'] and any(s['text']==c['quote'] for s in m['spans']) for m in dossier['owned_messages']))
                    source=dossier['evidence'][c['revision_id']]
                    self.assertEqual(source['body'][c['start_char']:c['end_char']],c['quote'])
                    self.assertEqual(hashlib.sha256(c['quote'].encode('latin1')).hexdigest(),c['text_sha256'])
                    self.assertEqual(source['body'][:c['start_char']].count('\n')+1,c['body_line'])

    def test_peer_beacons_do_not_create_own_rounds(self):
        self.assertEqual({e['round'] for e in self.accounts['P44']['events'] if e['status']=='observed'},{1})
        self.assertFalse(any(e['round']==4 and e['status']=='observed' for e in self.accounts['P31']['events']))

    def test_review_corrections_stay_applied(self):
        self.assertFalse(any(t['kind']=='followup' for t in self.accounts['C7e48e9024ab8/1']['timing']))
        t=next(t for t in self.accounts['C542786ec89f8/1']['timing'] if t['kind']=='followup')
        self.assertEqual(t['seconds'],65)
        self.assertIn('14:19:24',t['citation']['quote'])
        for e in self.accounts['Cc40ec18c27d8/1']['events']:
            self.assertFalse(e['round']==3 and e['status']=='predicted' and e['citation']['revision_id'].endswith('@11'))
            self.assertFalse(e['round']==4 and e['status']=='predicted' and e['citation']['revision_id'].endswith('@13'))
        e=next(e for e in self.accounts['C58a032ba14b5/1']['events'] if e['round']==2 and e['status']=='scheduled')
        self.assertIsNone(e['value'])
        self.assertTrue(any(e['status']=='inferred' for e in self.accounts['C439a0e1f791a/1']['events']))

    def test_split_histories_remain_distinct(self):
        self.assertIn('C7e48e9024ab8/1',self.accounts)
        self.assertIn('C7e48e9024ab8/2',self.accounts)
        locations={a['id']:t['id'] for t in self.tasks for a in t['accounts']}
        self.assertNotEqual(locations['C56f606951ca9/1'],locations['C56f606951ca9/2'])

if __name__=='__main__':unittest.main()
