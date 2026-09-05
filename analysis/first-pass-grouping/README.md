# First-pass wiki grouping workspace

This indexes all **14,591 retained wiki revisions on 4,579 pages** by exact editor names, candidate signoffs, and reply/addressee evidence. It is a candidate-enumeration workspace for assembling more trajectories. It does not merge these signals into identities or apply the existing 49 trajectories' membership judgments.

## Browse the groups

- [Editor-name groups](editor-index.md): **3,102 nonempty names**, plus one bucket containing **899 blank-editor revisions**. Every revision belongs to exactly one editor-field bucket.
- [Signoff groups](signoff-index.md): **4,349 occurrences of 1,097 literal tokens**. Signoffs are kept independent of editor names. Each dossier includes original source excerpts, page names, timestamps, and uncertainty flags.
- [Addressed-name reply groups](reply-index.md): **270 candidate lines addressing 153 literal names/cohort tokens**. These group possible recipients; they do not prove receipt or resolve shortened names into agent identities.
- [All reply/request candidates](replies.csv): **2,524 lines**, including requests without a resolved addressee. Sender editor, same-line signoffs, target candidates, cues, and exact excerpts are separate fields.
- [Editor/signoff pairings](editor_signoff_pairs.csv): **1,823 observed pairs**, useful for discovering inconsistent names. **328 editors** occur with multiple signoffs; **301 signoffs** occur under multiple editors.
- [Review queue](review_queue.csv): one row per editor/signoff group, with empty fields for your candidate trajectory ID, decision, rule tags, and notes. Priority labels describe evidence availability or collisions, not confidence in an agent identity.

The groups overlap. Their counts are not agent counts and must not be added together. Signoff/reply records can be inherited or repeated text in a replacement span, rather than separate newly authored messages.

## Suggested audit flow

1. Start with an editor or signoff dossier. Compare its actual task claims, schedules and page contexts before deciding whether the group should split.
2. Follow observed editor/signoff pairings as leads. A shared name never automatically pulls the other name's entire history into a trajectory.
3. Inspect reply evidence and page context. An addressed token, a request, a page link, and a confirmed response are different kinds of evidence. Preserve the peer's authorship when associating a reply.
4. Record your inclusion/exclusion rules and decisions separately. This workspace leaves conflicting, ambiguous, unsigned and cross-posted evidence available for review.

## Relationship to the existing 49

Source revisions are cross-referenced against the original dossier anchors and the frozen input under `analysis/trajectory-audit-49/input/`. A reference means that a revision appears there; it does **not** mean the whole revision, editor, signoff group, or peer message belongs to that trajectory. The `author_id`, input level and reference source are retained in `data/trajectory_references.jsonl` and SQLite.

No files in the 49-trajectory audit or live explorer were changed. New audit verdicts are not silently imported. Regenerating this workspace may update the reference snapshot if its upstream inputs change.

## What is retained and what remains uncertain

- Editor grouping covers every revision, including unsigned edits, deletions represented as saved revisions, probes, caches, and unrelated task material. Separate deletion-event logs are not treated as edits with available deleted bodies.
- Signoff extraction retains all 4,059 previous occurrence keys and adds **286 unique revision/line/token keys**. Four tokens occur twice on a line, so occurrence counts differ slightly from unique-key counts. Wiki-link signoffs such as `-- [[Name]]` and bounded context for standalone signatures are included.
- Same-page repeats, cross-posts, inherited replacement text, ambiguous ordinary words, punctuation-like markers, and multiple signoffs are retained with flags. A repeated standalone signature alone does not show its preceding message was copied. There is no arbitrary time-gap rule that splits or merges identities.
- Reply extraction uses English addressing/request/acknowledgement cues. It can miss implicit, multiline or differently phrased exchanges; capitalized ordinary nouns can be false target names. An exact target-name match is only a textual match.
- The conservative [page-link ledger](data/page_links.jsonl) preserves **2,085 directed page-reference pairs** from the previous extraction. The broader [page-reference scan](data/broad_page_references.jsonl) retains **35,964 changed lines** with links or known-page mentions, including navigation and code. Neither ledger establishes interaction or common authorship.
- Archive UTC orders records. Scaffold/task clocks remain untouched in the text for later audit. Page-family labels describe the host page and may not describe an observer's task.
- All original bodies and excerpts retain their byte-preserving archive representation. Original bytes round-trip through Latin-1; all body hashes pass. No archived command, URL, script, or counter endpoint was executed.

## Files and lookup

`grouping.sqlite` provides indexed `edits`, `signoffs`, `replies`, `reply_targets`, `page_links`, and `trajectory_references` tables. JSON `payload` columns retain full evidence. `data/edits.jsonl` contains full revision bodies and insert/replace spans; Markdown editor dossiers provide bounded previews and identify truncation.

CSV files are spreadsheet browsing views. Cells beginning with spreadsheet formula characters are prefixed with an apostrophe; JSONL and SQLite preserve exact names and text.

```sh
python analysis/first-pass-grouping/lookup.py --editor OpenAIJan18Scout
python analysis/first-pass-grouping/lookup.py --signoff OpenAIJan18Scout --limit 0
python analysis/first-pass-grouping/lookup.py --target Nov27
python analysis/first-pass-grouping/lookup.py --revision 'dse~OpenAIJan18FastCVD@3'
```

`--editor ''` selects blank editor fields. Names are case-sensitive. `--limit 0` prints all matching records. Full revision lookups include inherited peer text and must not be interpreted as ownership of the complete page.

## Reproduce

Run these commands from the original workspace root. They use only Python's standard library and local files. Rebuilding overwrites generated review queues, so keep completed decisions in a separate file.

```sh
python analysis/first-pass-grouping/rebuild.py
```

This reruns both extractors, preserves their separate research summaries, rebuilds the indexes and dossiers, and validates the result. The lower-level scripts are also available for adjusting candidate rules.

[Summary](summary.json), [validation results](validation.json), [signoff extraction review](research/signoff-review.md), [reply extraction limitations](research/reply-summary.json).
