# Conservative trajectory assembly

This is a separate, versioned assembly workspace. It does not overwrite the original 49-trajectory audit, the broad first-pass groupings, or the live explorer.

The current checkpoint contains **192 new reported trajectories from 200 candidate groups**, reviewed in four batches. The latest [batch004](batches/004/REPORT.md) adds **45 new histories and one existing-history extension** after independently auditing all 50 candidate groups and 287 observations. Eight groups are deferred across the four batches; incompatible same-signature histories remain split or held, and two independently confirmed alias bridges merge proposals into their canonical histories. Together with the original baseline there are 241 reported histories, including one provisional unsigned baseline history. This is not an authenticated agent count. Batch005 is the next queued batch; 450 screened multi-post groups and 399 other groups remain, plus the separate known-signature follow-up queue.

## Outputs

- `baseline/audited49.json`: original 49 with the nine audit corrections applied. Contains 48 supported histories and one provisional unsigned Aug21 history; 343 owned records including the P34 span recovery, 27 separately attributed peer records, six unassigned records and one excluded duplicate. P42's inherited table is trimmed. P43's legacy signed display name is not treated as an established alias.
- `INDEX.md`, `new-trajectories.json`, `trajectories.csv`: only independently audited new batches whose correction gate has opened. Each trajectory dossier preserves owned spans, peer context, excluded and unresolved observations.
- `candidate-status.json`, `summary.json`: completed dispositions and remaining work. These are candidate-group and reported-trajectory counts, not agent counts.
- `RUN-REPORT.md`: batch acceptance totals, audit results and deferred groups. `follow-up-candidates.json` preserves full unresolved decisions and deferred proposals.
- `accepted-fingerprints.json`: refreshed comparison index for detecting aliases against accepted histories. P43's legacy name remains explicitly unverified.
- `export-validation.json`: exact source-offset/hash checks and cross-trajectory ownership-overlap checks for the exported set and the original baseline.
- `batches/NNN/`: exact candidate packets, proposed assembly partitions, independent reviews, applied corrections and validation/gate status.

## Evidence and review policy

The source is the complete supplied wiki archive. Exact signatures retrieve candidate groups; they do not define agent identities. The initial screen selects groups with at least two distinct timed lines after downranking inherited, ambiguous and duplicate-line observations. This is a scheduling aid, not a membership test. It does not discover every possible unsigned, clockless or differently signed trajectory.

Each candidate group is reviewed for substantive own-task continuity, fresh owned spans, distinctive schedule landmarks, conflicts, corrections and cross-posts. At least two nonduplicate substantive owned contributions in two distinct publication revisions are required for new assembly; copies alone cannot satisfy the requirement. Internally cohesive material surviving only in one snapshot stays deferred under this policy. Insufficient groups stay deferred. Reused names with incompatible own histories split. The original 49 are checked as potential existing histories rather than silently duplicated.

Every supplied observation receives an include, associate, exclude or unresolved decision, with a reason and R01–R14 rules. Typed clock claims preserve ownership, system, task date, round/event kind, raw value, reported/predicted/inferred status and correction links where known. Missing context stays explicit. Exact spans and original revision/diff-base references are retained; source claims remain reported claims, not verified backend events.

A targeted independent recheck carried later clock-typing lessons back into batch001: 18 bare confirmation/history times were reclassified from exact prompt arrival to an unspecified event subtype, preserving the literal time and membership. The before snapshot, proposed corrections and source-reviewed resolutions are in `research/batch001-confirmation-recheck-*`. Batch001's initial pre-audit assembly was not separately frozen; its audit and resolution files preserve the original findings. Batches002–004 retain complete `proposed-*.json` snapshots before their independent reviews.

After approximately 50 candidate groups are assembled, different reviewers inspect all proposed assignments. No next batch starts until the review issues are resolved and source/coverage validation passes. Reviewers can correct or defer a proposal. Repeated reviewers do not create independent underlying evidence, and these audits do not establish statistical false-positive rates.

`source_char_positions` retains all occurrences when a literal excerpt repeats inside a revision. Where possible, the signoff body line selects `start_char`/`end_char`; otherwise location ambiguity remains explicit. Observation records can share a publication revision: `owned_publication_count` counts distinct retained revision IDs and is not an independent task-event count.

## Reproduce local outputs

```sh
python analysis/trajectory-assembly/prepare_baseline.py
python analysis/trajectory-assembly/validate_batch.py 001
python analysis/trajectory-assembly/validate_batch.py 002
python analysis/trajectory-assembly/validate_batch.py 003
python analysis/trajectory-assembly/validate_batch.py 004
python analysis/trajectory-assembly/batches/004/check_batch.py
python analysis/trajectory-assembly/export.py
python analysis/trajectory-assembly/verify_export.py
```

These scripts validate/export recorded review decisions; they do not pretend to reproduce human-style semantic judgment automatically. `PROTOCOL.md` specifies the assembly/audit record formats. The inherited audit rules are frozen in `research/RULES-v1.md`, with input hashes in `research/input-manifest.json`.

Keep review decisions and frozen candidate inputs together. Do not promote a candidate to an anchor merely because another candidate repeats it, and do not use editor-name transitivity to merge histories.
