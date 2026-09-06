# CVD agent accounting — 6 September 2026

**58 distinguishable, corroborated CVD agent/run histories** are supported by the retained wiki evidence. This comprises the prior 31 histories plus 27 additions. **23 further candidate schedules remain provisional and are excluded from that count.** Their sum, 81, is a roster of supported histories and candidate branches, not an authenticated agent total or an upper bound.

The counting unit is a reported single-task run. We use fresh own-task contributions, task-clock consistency, event type and distinctive schedule progression, rather than counting editor labels or signoffs. Without original process identifiers, the evidence cannot establish that each history corresponds to a physically distinct backend agent. The single-task assumption is explicit and matches the existing reconstruction rules.

## What changed

- Rechecked all 31 existing CVD histories. No supported merge or new split was warranted. All 235 pre-existing owned spans match the source text, coordinates and original Latin-1 byte hashes.
- Reviewed 97 broad signature candidate groups, including aliases, other-task contributors and peer mentions. Two reviewers worked disjoint partitions and cross-reviewed their proposals against the archive and diff bases.
- Reviewed 48 additional unsigned/broader revisions outside those signature packets. This recovered an unsigned Nov20/Nov21 history and strengthened existing histories without counting extra names.
- Accepted 27 new supported histories, including Dec26 under two signatures and the unsigned Nov20/Nov21 continuity. Supported additions retain at least two substantive nonduplicate contributions in different publication revisions.
- Preserved 23 provisional schedules, including single-publication histories, repeated-only reports, and unexplained clock branches. Generic data requests and probes do not create extra counted agents.
- Added ten unsigned owned spans across six revisions to four existing histories. Earlier audit decisions and IDs remain intact.
- Added 78 selected own round/clock events for the 27 supported additions. This is selected extraction, not an exhaustive transcription. Forecasts and scheduling expectations remain distinct from reported arrival/completion; no selected new R6 event is classified observed.

## Decisive examples

| Evidence | Accounting decision |
|---|---|
| `OpenAIJul09CVD` reports R1 11:34:16 / R5 13:02:14 and separately R1 06:41:01 / R5 08:08:56. | Retain two supported histories despite the same signoff. |
| Nov28 changes from `OpenAINov28CVD` to `OpenAINov28CVDLive`, preserving R1 23:39:18 and R6 due 01:27:23/24 with continuing survival reports. | One supported history despite the renamed signoff. |
| `OAI7C97Dec26` and `OpenAIHealthdataCVDDec26` share R5 20:56:43 / R6 due 22:20:08 and continuous outreach. | One newly supported Dec26 history. |
| Nov20 cohort explicitly uses task date Nov21, R3 due 01:10:22 then R4 due 02:33:48, and own current clock 01:45 → 02:10. Its posts address another Nov21 cohort as a peer. | One newly supported unsigned/mixed-signature history, separate from the addressed peer. |
| Nov01's isolated R5 due 02:53:55 conflicts with its supported 12:54:18 schedule. | Provisional unresolved branch, not a confirmed second agent and not a silently corrected time. |
| Jan02 has seven status paragraphs in one retained page creation. | One provisional history, not seven publications or a supported multi-publication history. |

There are weaker cases within the supported set: Aug16 relies on current-clock progression within a specific exchange rather than repeated exact round landmarks. Jul21's minute-only R6 forecast overlaps another run's clock, and Jun26's clocks are close to Nov01's; neither supplies enough evidence for a merge or a confirmed additional agent. These qualifications remain in the dossiers and visualiser.

## Dataset and visualiser

`trajectory-explorer/public/data/cvd-accounting/accounting.json` provides the full accounting; the repository-wide `TRAJECTORIES.csv` includes all supported and provisional entries. `dossiers.json`, `rounds.json`, and `extensions.json` are the reviewed task-dataset add-on. `coverage-ledger.json` resolves the unsigned/broader retrieval pass; `candidates-a.json` and `candidates-b.json` preserve group decisions. The original candidate proposals and independent reviews remain available, with applied changes recorded in `resolutions.json`.

The `/tasks` CVD group now exposes an **Agent accounting** tab. It separates supported/provisional rosters, searches names/dates/clocks, explains splits and aliases, and opens exact publication evidence. The 27 supported additions also enter the normal rounds matrix and trajectory evidence browser. Provisional entries remain excluded from matrix totals. Across all task families, the browser now contains 298 supported histories plus 24 provisional entries (the 23 CVD candidates and the original P43).

## Validation and reproduction

All **374 retained owned spans** across this CVD accounting, including provisional evidence, match original source text and byte hashes. Supported histories have no cross-history overlapping owned source spans. Independent review corrections include: Feb07 arrival cites the actual confirmation, Jun09 “done” remains completion rather than an asserted answer timestamp, generic topic-only posts move to associated context, forecast alternatives and corrections are preserved, and a round-range country-list parsing error was removed.

From the workspace root:

```sh
python trajectory-explorer/scripts/build_task_trajectories.py
python trajectory-explorer/scripts/build_audited_tasks.py
python -m unittest discover -s trajectory-explorer/scripts -p 'test_cvd_accounting.py'
```

`review-gate.json` binds the accepted inputs and reports to hashes; exporters verify it before loading the add-on. Reconstruction scripts preserve the existing baseline and family-completion inputs. Regenerating does not reproduce semantic review: frozen proposals, independent findings, and explicit resolutions are part of the required inputs.

This public snapshot preserves the existing archive redactions. The CVD reviewed inputs live under `trajectory-explorer/research/cvd-accounting/`; the reproduction commands above use its refreshed public-release acceptance gate.
