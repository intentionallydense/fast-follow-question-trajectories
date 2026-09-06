"""Guard the accounting boundary and the source mistakes caught during CVD review."""
import json
import unittest
from build_task_trajectories import ROOT
from cvd_data import cvd_data, gate

class CvdAccounting(unittest.TestCase):
    def test_supported_and_provisional_totals_stay_separate(self):
        accounting=cvd_data('accounting.json')
        task=json.loads((ROOT/'public/data/audited-tasks/ihme-cvd-deaths.json').read_text())
        supported={r['id'] for r in accounting['roster'] if r['status']=='supported'}
        provisional={r['id'] for r in accounting['roster'] if r['status']=='provisional'}
        self.assertEqual(len(supported),58)
        self.assertEqual(len(provisional),23)
        self.assertEqual({a['id'] for a in task['accounts']},supported)
        self.assertFalse(supported & provisional)
        self.assertEqual(gate()['status'],'passed')
        self.assertIn('CVD-B03-second',provisional)
        self.assertTrue({'C7e48e9024ab8/1','C7e48e9024ab8/2','P34','cvd-dec26-slow','CVD-Nov20-7c97'}<=supported)

    def test_forecasts_cannot_become_observed_country_claims(self):
        rounds={r['trajectory_id']:r for r in cvd_data('rounds.json')}
        for r in rounds.values():
            for e in r['events']:
                if e['round']==6:self.assertNotEqual(e['status'],'observed')
        feb=rounds['cvd-feb07-fast']['events']
        self.assertTrue(any(e['round']==5 and e['status']=='observed' and e['revision_id']=='dse~OpenAICVDDec08Fast2028@25' for e in feb))
        self.assertFalse(any(e['round']==5 and e['target']=='Armenia' for e in rounds['cvd-feb20-2027-fast']['events']))
        jun=next(d for d in cvd_data('dossiers.json') if d['trajectory_id']=='cvd-jun09-fast')
        self.assertTrue(any(c['raw_value']=='11:55:20' and c['event_kind']=='completion' for c in jun['schedule_claims']))

    def test_reviewed_extensions_and_generic_context_are_separate(self):
        extensions=cvd_data('extensions.json')
        self.assertEqual(len(extensions),6)
        self.assertEqual(sum(len(m['spans']) for m in extensions),10)
        for m in extensions:
            d=json.loads((ROOT/'public/data/assembled-trajectories'/(m['trajectory_id'].replace('/','-')+'.json')).read_text())
            self.assertIn(m,d['owned_messages'])
        for tid,rid in [('cvd-dec08-2028-fast','dse~OpenAICVDDec08Fast2028@30'),('cvd-jan31-slow','dse~HealthdataCVDSequenceCollab@63'),('CVD-B33','dse~HealthdataCVDSequenceCollab@56')]:
            d=next(d for d in cvd_data('dossiers.json') if d['trajectory_id']==tid)
            self.assertFalse(any(m['revision_id']==rid for m in d['owned_messages']))
            self.assertTrue(any(m['revision_id']==rid for m in d['associated_messages']))

if __name__=='__main__':unittest.main()
