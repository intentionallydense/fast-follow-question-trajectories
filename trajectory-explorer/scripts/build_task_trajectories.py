"""Export audited assembly dossiers for task cards without inferring new round claims."""
import hashlib
import json
import re
import zipfile
from pathlib import Path
from cvd_data import cvd_data, with_cvd_extensions

ROOT = Path(__file__).resolve().parents[1]
ASSEMBLY = ROOT.parent / 'analysis/trajectory-assembly'
COMPLETION = ROOT / 'research/family-completion'

def completion_data(name):
    path = COMPLETION / name
    return json.loads(path.read_text()) if path.exists() else []
BASELINE_TASKS = {'sector': 'datausa-sector61-state', 'CVD': 'ihme-cvd-deaths',
 'construction_ny': 'datausa-construction-workforce-ny', 'clothing': 'datausa-clothing-workforce',
 'FP': 'ihme-family-planning', 'OECD-equity': 'oecd-preprimary-private-spending',
 'grocery': 'datausa-grocery-workforce', 'RRP': 'oecd-regional-co2'}
# Match reviewed dossier task descriptions, never signatures, editors or peer text.
RULES = [
 (r'police', 'datausa-police-wage-age'), (r'french|cajun', 'datausa-language-french'),
 (r'occupation salary|occupation wages sector|school psychologists', 'datausa-occupation-salary-61-62'),
 (r'^(?!.*(?:salary|occupation wages)).*sector61', 'datausa-sector61-state'), (r'county poverty|poverty county', 'datausa-poverty-county'),
 (r'poverty.*state', 'datausa-poverty-state'),
 (r'construction.*wage|electricians', 'datausa-construction-wage'),
 (r'construction.*2016/2018', 'datausa-construction-workforce-ny'),
 (r'arizona construction|construction.*AZ', 'datausa-construction-workforce-az'),
 (r'CVD|cardiovascular', 'ihme-cvd-deaths'), (r'cashiers.*masters', 'datausa-cashiers-masters'),
 (r'cashiers.*bachelors', 'cashiers-bachelors-2015'),
 (r'production.occupation', 'datausa-production-share'), (r'finance', 'datausa-finance-gender-gap'),
 (r'maids', 'datausa-maids-wage'), (r'OECD', 'oecd-preprimary-private-spending'),
 (r'clothing', 'datausa-clothing-workforce'), (r'grocery', 'datausa-grocery-workforce'),
 (r'transportation', 'datausa-transport-production'), (r'UEFA', 'uefa-pass-accuracy'),
 (r'family planning', 'ihme-family-planning'), (r'SDG', 'sdg-index-score'),
 (r'Asian enrollment', 'datausa-enrollment-asian'),
]

def task_id(t):
    if 'task_id' in t:
        inventory = {r['task_id'] for r in completion_data('inventory.json')}
        assert t['task_id'] in inventory
        return t['task_id']
    if 'task_family' in t:
        return BASELINE_TASKS[t['task_family']]
    if t['trajectory_id'] == 'C556a612bd1ee/1':
        return 'ihme-lymphatic-filariasis'  # LF page explicitly defines the initial task; see family completion correction.
    matches = {target for pattern, target in RULES if re.search(pattern, t['task'], re.I)}
    if len(matches) != 1:
        raise ValueError((t['trajectory_id'], t['task'], matches))
    return matches.pop()

def main():
    baseline = json.loads((ASSEMBLY / 'baseline/audited49.json').read_text())
    new = json.loads((ASSEMBLY / 'new-trajectories.json').read_text())
    additions = completion_data('dossiers.json')
    if additions:
        review = json.loads((COMPLETION / 'review-gate.json').read_text())
        assert review['status'] == 'passed'
        assert set(review['trajectory_ids']) == {t['trajectory_id'] for t in additions}
        for name, digest in review['accepted_sha256'].items():
            assert hashlib.sha256((COMPLETION / name).read_bytes()).hexdigest() == digest, name
    new += additions
    new += cvd_data('dossiers.json')
    tasks = set(BASELINE_TASKS.values()) | {target for _, target in RULES}
    tasks |= {r['task_id'] for r in completion_data('inventory.json')}
    with zipfile.ZipFile(ROOT.parent / 'full-wiki-logs.zip') as archive:
        sources = {r['rev_id']: dict(r, jsonl_line=i) for i, line in enumerate(archive.read('revisions.jsonl').splitlines(), 1) for r in [json.loads(line)]}
    dest = ROOT / 'public/data/assembled-trajectories'
    dest.mkdir(parents=True, exist_ok=True)
    roster = []
    for t in baseline + new:
        t = with_cvd_extensions(t)
        tid = task_id(t)
        assert tid is None or tid in tasks
        file = t['trajectory_id'].replace('/', '-') + '.json'
        evidence = {}
        for group in ['owned_messages', 'associated_messages', 'unassigned', 'excluded']:
            for m in t[group]:
                rid = m.get('revision_id')
                if rid not in sources:
                    continue
                s = sources[rid]
                evidence[rid] = dict(revision_id=rid, jsonl_line=s['jsonl_line'], server_time=s['time'], recorded_editor=s['label'], body=s['body'])
                for span in m.get('spans', []):
                    assert s['body'][span['start_char']:span['end_char']] == span['text'], (t['trajectory_id'], rid)
                    assert hashlib.sha256(span['text'].encode('latin1')).hexdigest() == span['text_sha256']
                base = m.get('diff_base')
                if base in sources:
                    b = sources[base]
                    evidence[base] = dict(revision_id=base, jsonl_line=b['jsonl_line'], server_time=b['time'], recorded_editor=b['label'], body=b['body'])
        dossier = dict(t, evidence=evidence)
        corrections = completion_data('existing-trajectory-corrections.json')
        correction = next((c for c in corrections if c['trajectory_id'] == t['trajectory_id']), None)
        if correction:
            dossier['classification_correction'] = correction
            dossier['original_task_description'] = dossier['task']
            dossier['task'] = correction['task']
            dossier['task_id'] = correction['task_id']
        (dest / file).write_text(json.dumps(dossier, ensure_ascii=False) + '\n')
        title = 'Lymphatic filariasis · Nov14 year follow-up' if t['trajectory_id'] == 'C556a612bd1ee/1' else t.get('task', t.get('task_family'))
        roster.append(dict(id=t['trajectory_id'], task_id=tid, title=title,
            name=t.get('self_name', t.get('display_name')), status=t['status'], batch=t.get('batch'),
            owned_count=len(t['owned_messages']), publication_count=len({m['revision_id'] for m in t['owned_messages']}),
            rationale=t.get('membership_rationale', 'Baseline membership follows the corrected 49-trajectory audit. See each retained span for its attribution rationale.'),
            file='/data/assembled-trajectories/' + file))
    assert len({t['id'] for t in roster}) == len(roster)
    result = dict(trajectories=roster, baseline_count=len(baseline), new_count=len(new),
        unmapped_count=sum(t['task_id'] is None for t in roster))
    (ROOT / 'app/tasks/assembled-index.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'public/data/assembled-trajectories.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f"Exported {len(roster)} histories; {result['unmapped_count']} without an existing task card; verified exact spans and hashes.")

if __name__ == '__main__':
    main()
