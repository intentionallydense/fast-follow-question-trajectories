"""Exact, case-sensitive overlap of source-revision labels for accepted owned spans."""
import collections
import csv
import hashlib
import itertools
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ASSEMBLY = OUT.parent / 'trajectory-assembly'
inputs = ['baseline/audited49.json', 'new-trajectories.json']
trajectories = sum((json.loads((ASSEMBLY / f).read_text()) for f in inputs), [])
by_editor = collections.defaultdict(list)
rows = []
for t in trajectories:
    publications = {m['revision_id']: m for m in t['owned_messages']}
    labels = collections.defaultdict(list)
    for rid, m in publications.items():
        labels[m['editor']].append(rid)
    row = dict(trajectory_id=t['trajectory_id'], name=t.get('signature', t.get('display_name')),
               status=t['status'], editors=dict(labels), editor_count=len(labels),
               owned_publication_count=len(publications))
    rows.append(row)
    for editor, revisions in labels.items():
        by_editor[editor].append(dict(trajectory_id=row['trajectory_id'], name=row['name'], revisions=sorted(revisions)))
shared = {e: refs for e, refs in by_editor.items() if len(refs) > 1}
affected = {r['trajectory_id'] for refs in shared.values() for r in refs}
pairs = set(pair for refs in shared.values() for pair in itertools.combinations(sorted(r['trajectory_id'] for r in refs), 2))
revision_sets = {r['trajectory_id']: {rid for revs in r['editors'].values() for rid in revs} for r in rows}
single_label_groups = collections.defaultdict(list)
for r in rows:
    if r['editor_count'] == 1:
        single_label_groups[next(iter(r['editors']))].append(r['trajectory_id'])
summary = dict(
    trajectories=len(rows), distinct_editor_labels=len(by_editor),
    single_editor_trajectories=sum(r['editor_count'] == 1 for r in rows),
    multiple_editor_trajectories=sum(r['editor_count'] > 1 for r in rows),
    maximum_editors_per_trajectory=max(r['editor_count'] for r in rows),
    shared_editor_labels=len(shared), trajectories_sharing_any_editor=len(affected),
    trajectories_without_shared_editors=len(rows) - len(affected),
    editor_count_distribution=dict(sorted(collections.Counter(r['editor_count'] for r in rows).items())),
    trajectory_pairs_sharing_editor=len(pairs),
    sharing_pairs_with_same_source_revision=sum(bool(revision_sets[a] & revision_sets[b]) for a, b in pairs),
    single_editor_trajectory_groups_sharing_their_only_label={e: ids for e, ids in single_label_groups.items() if len(ids) > 1},
    scope='All 196 accepted/provisional reconstructed histories. Only owned_messages; distinct revision IDs per trajectory. Exact case-sensitive source editor labels, not authenticated identities. Peer, excluded, unresolved and deferred records omitted.',
    source_hashes={f: hashlib.sha256((ASSEMBLY / f).read_bytes()).hexdigest() for f in inputs},
)
(OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
(OUT / 'trajectory-editors.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
(OUT / 'shared-editors.json').write_text(json.dumps(shared, ensure_ascii=False, indent=2) + '\n')
with (OUT / 'trajectory-editor-publications.csv').open('w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['trajectory_id', 'trajectory_name', 'source_editor_label', 'revision_id'])
    for r in rows:
        for e, revisions in r['editors'].items():
            for rid in sorted(revisions): writer.writerow([r['trajectory_id'], r['name'], e, rid])
lines = ['# Editor-label overlap across 196 trajectories', '', summary['scope'], '',
         'The measured field is `label` in revisions.jsonl, exported as `editor` in the trajectory artifacts. It is revision metadata; it need not equal the signoff or the owner of every source span. These results do not merge trajectories.', '',
         '| Measure | Count |', '| --- | --- |',
         f"| Trajectories using one editor label | {summary['single_editor_trajectories']} |",
         f"| Trajectories using multiple editor labels | {summary['multiple_editor_trajectories']} |",
         f"| Trajectories sharing any editor label with another history | {len(affected)} |",
         f"| Trajectories whose editor labels are exclusive to that history | {len(rows) - len(affected)} |",
         f"| Distinct editor labels | {len(by_editor)} |",
         f"| Editor labels appearing in multiple histories | {len(shared)} |", '',
         'One history can use multiple labels while none is shared with another history; these are separate measurements. The maximum is 14 labels within a history. There are 95 trajectory pairs sharing a label; only two of those pairs also share a source revision.', '',
         '## All shared editor labels', '', '| Exact editor label | Number of histories | Histories (owned publication counts) |', '| --- | --- | --- |']
for editor, refs in sorted(shared.items(), key=lambda x: (-len(x[1]), x[0])):
    descriptions = '; '.join(f"{r['name']} [{r['trajectory_id']}] ({len(r['revisions'])})" for r in refs)
    lines.append(f"| {editor.replace('|', chr(92) + '|')} | {len(refs)} | {descriptions} |")
lines += ['', 'Full revision-level evidence is in `trajectory-editor-publications.csv`; per-history sets are in `trajectory-editors.json`. Counts describe labels attached to accepted publications, not verified agent identity.']
(OUT / 'REPORT.md').write_text('\n'.join(lines) + '\n')
print(json.dumps(summary, indent=2))
