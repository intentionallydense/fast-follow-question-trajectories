"""Guard against silent losses or attribution changes in the task-facing assembly."""
import json
import hashlib
import unittest
from build_task_trajectories import ROOT, ASSEMBLY, task_id, completion_data
from cvd_data import cvd_data, with_cvd_extensions

class TaskTrajectories(unittest.TestCase):
    def test_all_accepted_dossiers_preserved(self):
        original = [with_cvd_extensions(t) for t in json.loads((ASSEMBLY/'baseline/audited49.json').read_text()) + json.loads((ASSEMBLY/'new-trajectories.json').read_text()) + completion_data('dossiers.json') + cvd_data('dossiers.json')]
        index = json.loads((ROOT/'app/tasks/assembled-index.json').read_text())
        rows = {t['id']: t for t in index['trajectories']}
        self.assertEqual(set(rows), {t['trajectory_id'] for t in original})
        for t in original:
            with self.subTest(trajectory=t['trajectory_id']):
                row = rows[t['trajectory_id']]
                exported = json.loads((ROOT/'public'/row['file'].lstrip('/')).read_text())
                evidence = exported.pop('evidence')
                exported.pop('classification_correction', None)
                if 'original_task_description' in exported:
                    self.assertEqual(exported['task_id'], 'ihme-lymphatic-filariasis')
                    exported['task'] = exported.pop('original_task_description')
                    exported.pop('task_id')
                self.assertEqual(exported, t)
                for message in t['owned_messages'] + t['associated_messages']:
                    self.assertIn(message['revision_id'], evidence)
                self.assertEqual(row['task_id'], task_id(t))
        self.assertEqual([r['id'] for r in rows.values() if r['task_id'] is None], [])
        self.assertEqual(rows['C556a612bd1ee/1']['task_id'], 'ihme-lymphatic-filariasis')
        self.assertEqual(rows['P43']['status'], 'provisional')

    def test_environment_claims_have_owned_auditable_sources(self):
        export = json.loads((ROOT/'public/data/assembled-environment.json').read_text())
        claims = export['claims']
        self.assertEqual(export['summary']['claim_count'], len(claims))
        self.assertEqual(len({c['id'] for c in claims}), len(claims))
        self.assertEqual(sum(export['summary']['task_counts'].values()), len(claims))
        for c in claims:
            with self.subTest(claim=c['id']):
                dossier = json.loads((ROOT/'public'/c['dossier_file'].lstrip('/')).read_text())
                self.assertTrue(any(m['revision_id'] == c['revision_id'] and any(s['text'] == c['quote'] for s in m['spans']) for m in dossier['owned_messages']))
                source = dossier['evidence'][c['revision_id']]
                self.assertEqual(source['body'][c['source']['start_char']:c['source']['end_char']], c['quote'])
                self.assertEqual(source['body'][:c['source']['start_char']].count('\n')+1, c['source']['body_line'])
                self.assertEqual(hashlib.sha256(c['quote'].encode('latin1')).hexdigest(), c['source']['text_sha256'])
                self.assertTrue(c['qualification'])

    def test_distinct_task_variants(self):
        examples = {
            'DataUSA occupation salary sector61-62 year2020': 'datausa-occupation-salary-61-62',
            'Sector61 state sequence May17 2m/13s tier': 'datausa-sector61-state',
            'Jan03 slow construction workforce 2016/2018 sequence': 'datausa-construction-workforce-ny',
            'Dec27 Arizona construction workforce 2016 sequence': 'datausa-construction-workforce-az',
            'DataUSA female electricians Construction average wage by year': 'datausa-construction-wage',
        }
        for label, expected in examples.items():
            self.assertEqual(task_id(dict(trajectory_id='test', task=label)), expected)
        with self.assertRaises(ValueError):
            task_id(dict(trajectory_id='test', task='Unknown task'))

if __name__ == '__main__':
    unittest.main()
