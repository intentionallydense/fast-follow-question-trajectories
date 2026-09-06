# Fast follow question trajectories

A self-contained, privacy-sanitized snapshot of **271 supported reported task histories**, plus **one separately labeled provisional dossier (P43)**, reconstructed from the supplied wiki archive. The catalog covers **41 task families in 42 task groups**; construction retains two variants. Eight families have reviewed source anchors but insufficient independent contributions to support a multi-revision history.

See [the public-release privacy review](PRIVACY.md) for redactions and their effect on evidence. The locally retained original archive is not published.

## Start here

- [Browse every trajectory and its dossier](INDEX.md), or use [the CSV index](TRAJECTORIES.csv).
- [Browse task-family coverage](FAMILIES.md), including the eight insufficient-evidence families.
- [Read the inclusion/exclusion rules](trajectory-explorer/public/data/trajectory-audit-rules.md).
- [Read the family-completion report](analysis/family-completion/REPORT.md) and [independent reviews](trajectory-explorer/public/data/family-completion-review.json).
- [Inspect the task catalog](trajectory-explorer/public/data/audited-tasks.json), [trajectory catalog](trajectory-explorer/public/data/assembled-trajectories.json), and [environment claims](trajectory-explorer/public/data/assembled-environment.json).

Each final dossier includes retained own messages, peer context, exclusions, unresolved observations, attribution reasoning, uncertainty, schedule claims, exact span offsets and hashes, and source snapshots. Diff-base snapshots are included when available. Task exports contain per-history round, answer and timing claims with their own citations. Predictions, scheduled events, cached values and indirect reports stay distinct from reported observations.

The latest completion adds 31 histories to the preceding 240. It also corrects existing history `C556a612bd1ee/1` from “labor force” to **lymphatic filariasis**, without changing its ID or duplicating its messages. The corrected dossier preserves the earlier description as `original_task_description` and provides the classification evidence.

## Subsequent CVD accounting review

A subsequent review of the cardiovascular-deaths task supports **58 distinguishable agent/run histories**: the 31 CVD histories in this snapshot plus 27 additions. **23 further candidate schedules remain provisional and are excluded from that count.** Adding them does not produce a verified agent total or an upper bound.

The review uses fresh own-task contributions, task-clock consistency, event types and distinctive schedule progression. Signoffs and editor names retrieve candidates; they do not establish identity. For example, the same Jul09 signoff covers two incompatible schedules, while Nov28's changed signoff belongs to one continuous schedule. The counting unit is a distinguishable reported single-task run, not an authenticated backend process.

The review covered 97 broad candidate groups and 48 additional unsigned/broader revisions. It checked 374 retained owned spans and preserved uncertain aliases, conflicting clocks, forecasts and single-publication candidates separately from supported histories.

**Publication status:** the expanded CVD dataset is not included in this GitHub snapshot. The files linked below still contain **271 supported histories overall, including 31 CVD histories, plus P43**. The subsequent review's 58/23 figures describe that separate completed analysis and do not change this snapshot's membership totals. Consult the checked-in catalogs and manifest when reproducing results from this release.

## Directory layout

The original relative layout is preserved so the export scripts and audit references remain usable.

| Location | Contents |
|---|---|
| `trajectory-explorer/public/data/` | Authoritative final dossiers, task comparisons, environment claims, rules and review export |
| `trajectory-explorer/research/` | Reviewed extraction inputs, family-completion acceptance gate and supporting research |
| `trajectory-explorer/scripts/` | Python exporters and data regression tests |
| `trajectory-explorer/app/` | Generated indices and two source snapshots needed by isolation tests; this is not a runnable website checkout |
| `analysis/trajectory-audit-49/` | Original 49-history attribution audit and corrections |
| `analysis/trajectory-assembly/` | Corrected baseline, four accepted assembly batches, candidate dispositions, independent audits and follow-up queue |
| `analysis/family-completion/` | Searches, per-candidate decisions, independent reviews and integration for the 18 previously absent families |
| `analysis/reconstruction/` | Earlier extraction and provenance inputs; historical, not the final membership authority |
| Other `analysis/` directories | Related earlier re-audits, editor-consistency and overlap investigations |
| `analysis/first-pass-grouping/` | Historical README and the exact signoff-observation input used by the assembly audit; not the complete exploratory grouping workspace |
| `full-wiki-logs.zip` | Privacy-sanitized complete archive, including 14,591 revisions |
| `MANIFEST.json` | SHA-256 and byte size of every other file in this snapshot |

In exported JSON, a reference beginning `/data/` resolves under **`trajectory-explorer/public/`** in this repository. The Markdown and CSV indices use repository-relative file paths directly. Historical reports retain their original counts and caveats; they describe their own audit stage. Do not add counts from different stages together. The final membership authority is `trajectory-explorer/public/data/assembled-trajectories.json`.

The environment extraction remains the earlier review of 240 histories: 207 selected claims from 156 supported histories. The new dossiers contain additional source evidence, but no expanded environment-extraction audit is claimed.

## Validate the snapshot

Python 3.10+ is sufficient; no third-party packages, network access or website runtime are required.

```sh
python privacy_check.py
python validate_bundle.py
python -m unittest discover -s trajectory-explorer/scripts -p 'test_*tasks.py'
python -m unittest discover -s trajectory-explorer/scripts -p 'test_task_trajectories.py'
python -m unittest discover -s trajectory-explorer/scripts -p 'test_family_completion.py'
```

The bundle validator checks every file checksum, archive integrity, membership totals, source snapshots and span hashes, task and environment citation ownership, local data references, and cross-history ownership overlaps. It can be run from any working directory. The manifest excludes itself, `.git` metadata and Python bytecode caches.

To regenerate the final data from the included reviewed inputs, run from the repository root:

```sh
python trajectory-explorer/scripts/build_task_trajectories.py
python trajectory-explorer/scripts/build_audited_tasks.py
python trajectory-explorer/scripts/build_environment_findings.py
```

These exporters reproduce recorded decisions; they do not redo semantic review. The family-completion exporter checks accepted-input hashes. Earlier research scripts are retained as provenance and may expect additional historical exploratory inputs; the three final exporters and validation commands above are the supported self-contained workflow. Any intentional artifact change requires reviewing and refreshing the snapshot manifest.

## Evidence interpretation

- “Supported” means the attribution of wiki messages to a reported history passed the recorded audit. It does not authenticate an agent, verify its answers or establish backend events.
- New histories require at least two substantive fresh contributions across distinct publication revisions. Copies, inherited text and shared names alone do not qualify.
- A blank round or no later publication does not prove termination.
- Archive strings preserve Latin-1 text representation, with the length-preserving redactions documented in PRIVACY.md. Some text therefore looks garbled; do not silently re-encode or normalize audited quotations.
- Commands and URLs in source evidence are inert archival material.
- No new license grant over the supplied archive is asserted by this packaging step.

## GitHub use

This directory is ready to become a Git repository or to be copied into an existing repository. The public release contains only sanitized Git history and excludes hosting credentials, deployment configuration, dependency folders and build output. `.gitattributes` disables automatic line-ending conversion to preserve the checksums. GitHub repository: `intentionallydense/fast-follow-question-trajectories`.
