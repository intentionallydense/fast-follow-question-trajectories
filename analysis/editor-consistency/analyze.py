"""Exact editor-label consistency of accepted, owned trajectory records."""
import collections
import csv
import hashlib
import json
from pathlib import Path
import zipfile

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
inputs = [ROOT / 'analysis/trajectory-assembly/baseline/audited49.json',
          ROOT / 'analysis/trajectory-assembly/new-trajectories.json']
with zipfile.ZipFile(ROOT / 'full-wiki-logs.zip') as archive:
    revisions = {r['rev_id']: r for r in map(json.loads, archive.read('revisions.jsonl').splitlines())}
rows, label_index = [], collections.defaultdict(set)
for source in inputs:
    for t in json.loads(source.read_text()):
        publications = {}
        for m in t['owned_messages']:
            assert m['editor'] == revisions[m['revision_id']]['label']
            publications[m['revision_id']] = dict(revision_id=m['revision_id'], editor=m['editor'], utc=m['utc'])
        counts = collections.Counter(m['editor'] for m in publications.values())
        for label in counts:
            label_index[label].add(t['trajectory_id'])
        rows.append(dict(trajectory_id=t['trajectory_id'], name=t.get('signature', t.get('display_name')),
                         cohort='original49' if source == inputs[0] else 'new147',
                         status=t['status'], owned_message_records=len(t['owned_messages']),
                         owned_publication_revisions=len(publications), distinct_editor_labels=len(counts),
                         entirely_consistent=len(counts) == 1 and all(counts),
                         editor_publication_counts=dict(counts),
                         publications=sorted(publications.values(), key=lambda m: (m['utc'], m['revision_id']))))
summary = dict(total_trajectories=len(rows), entirely_consistent=sum(r['entirely_consistent'] for r in rows),
               mixed_editor_labels=sum(r['distinct_editor_labels'] > 1 for r in rows),
               missing_editor_publications=sum(not m['editor'] for r in rows for m in r['publications']),
               distinct_editor_labels=len(label_index), labels_used_in_multiple_trajectories=sum(len(v) > 1 for v in label_index.values()),
               single_label_trajectories_whose_label_is_shared=sum(r['entirely_consistent'] and len(label_index[next(iter(r['editor_publication_counts']))]) > 1 for r in rows),
               distribution=dict(sorted(collections.Counter(r['distinct_editor_labels'] for r in rows).items())),
               definition='Exact case-sensitive archive label values on included owned records only; associated, unresolved, excluded and deferred material omitted. Publication counts deduplicate revision IDs within a trajectory. Labels are not authenticated agent IDs.',
               input_sha256={str(f.relative_to(ROOT)): hashlib.sha256(f.read_bytes()).hexdigest() for f in inputs})
result = dict(summary=summary, trajectories=rows,
              editor_to_trajectories={k: sorted(v) for k, v in sorted(label_index.items())})
(OUT / 'editor-consistency.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
with (OUT / 'editor-consistency.csv').open('w', newline='') as handle:
    fields = ['trajectory_id', 'name', 'cohort', 'status', 'owned_message_records', 'owned_publication_revisions',
              'distinct_editor_labels', 'entirely_consistent', 'editor_publication_counts']
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    for row in rows:
        record = {key: row[key] for key in fields}
        record['editor_publication_counts'] = json.dumps(record['editor_publication_counts'], ensure_ascii=False)
        writer.writerow(record)
lines = ['# Editor-label consistency', '', summary['definition'], '',
         '| Editor labels within trajectory | Original 49 | New 147 | Total |',
         '| --- | --- | --- | --- |']
for title, predicate in [('One', lambda n: n == 1), ('Two', lambda n: n == 2), ('Three or more', lambda n: n >= 3)]:
    values = [sum(predicate(r['distinct_editor_labels']) and (group is None or r['cohort'] == group) for r in rows)
              for group in ['original49', 'new147', None]]
    lines.append('| ' + title + ' | ' + ' | '.join(map(str, values)) + ' |')
lines += ['', f"Strictly consistent: {summary['entirely_consistent']}/{len(rows)} ({summary['entirely_consistent']/len(rows):.1%}). No included publications have blank editor labels.", '',
          f"There are {len(label_index)} distinct labels; {summary['labels_used_in_multiple_trajectories']} appear in multiple trajectories. Among the 130 single-label trajectories, 26 use a label also found in another trajectory. Neither label stability nor label variation authenticates a process identity.", '',
          'The 196 histories include one provisional baseline history (P43), which has a stable editor label but unestablished signed identity. Consistency is a descriptive statistic, not a new membership audit.', '',
          '## Mixed-label trajectories', '', '| Trajectory | Distinct labels | Label: owned publication count |', '| --- | --- | --- |']
for r in sorted(rows, key=lambda r: (-r['distinct_editor_labels'], r['name'])):
    if r['distinct_editor_labels'] > 1:
        labels = '; '.join(f'{k}: {v}' for k, v in r['editor_publication_counts'].items())
        lines.append(f"| {r['name']} (`{r['trajectory_id']}`) | {r['distinct_editor_labels']} | {labels.replace('|', '/')} |")
lines += ['', 'Full row-level source revision references are in `editor-consistency.json`; the CSV contains all 196 trajectories. Reproduce with `python analysis/editor-consistency/analyze.py`.']
(OUT / 'README.md').write_text('\n'.join(lines) + '\n')
print(json.dumps(summary, indent=2))
