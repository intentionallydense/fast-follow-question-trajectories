# Audit of the latest 147 trajectories

The review covers the final 147 reported trajectories from 150 candidate groups in batches001–003, against the original 49-trajectory audit's R01–R14 rules. Three reviewers covered separate batches; the coordinating review checked baseline and cross-batch collisions, source integrity, disputed decisions and exact replacement spans.

The core task histories remain supported; the review recommends message-level and metadata corrections. No new whole-trajectory merge, split or deletion was established. The original 48 supported plus one provisional baseline histories are comparison evidence, not newly audited identities. These are reconstructed reported histories, not an authenticated agent census.

## Membership and span findings

| Action | Observation(s) | Reason |
|---|---|---|
| Expand retained signed blocks | FP-S004196, FP-S002731, FP-S003237, FP-S001623 | Recover fresh task/schedule content governed by a signoff or explicitly continuing its distinctive own schedule. The Jun01 confirmation follows its signed request. Preserve peer-derived predictions as such. |
| Recover owned outreach | FP-S001504, FP-S001505, FP-S001506 | The Jul03 signal instructions continue its accepted timed Oct16 exchange and established signal plan. Preserve three destination publications with cross-post dependencies; copies do not authenticate each other. |
| Trim owned span | FP-S000358 | Remove the generic German wiki placeholder from the Aug01 clothing founding report. Keep the signed task report. |
| Recover signed founding blocks | FP-S003443, FP-S000185 | The Nov28 OECD and ResearchHelper clothing reports have substantive own schedule bridges in the paragraphs preceding their signoffs. Keep Feb08/Jan29 peer paragraphs out of ResearchHelper's owned spans. |
| Hold owned assignments unresolved | FP-S001343, FP-S000472 | The Oct30 request refers to Jan06's clock and follows other speakers; the Jan29 monitoring ping provides a generic request with name/date/family. Neither supplies the claimed specific own-task continuation. Their timed trajectory cores survive. |

These are five recoverable observation assignments, four expansions of existing owned records, one partial trim and two proposed ownership holds. Observation counts are not independent event counts. Exact evidence, rule IDs and proposed retained text are in the batch JSON reviews and consolidated findings.

## Other corrections and disputed cases

Clock metadata still sometimes converts a bare round history or confirmation into an exact prompt-arrival claim. Preserve the raw value but use an unspecified round-event subtype unless explicit arrival evidence supports it. Keep timer duration distinct from deadline; keep receipt/transition time distinct from the underlying event. The inferred time of an unidentified counter hit must not become an owned task event. Preserve explicit correction relationships and predicted/observed distinctions.

Three scratch/cache-test originals, FP-S000854, FP-S000356 and FP-S002509, lack an ownership bridge and should be **unresolved**, following the initial audit's P47 precedent. Lack of evidence is not affirmative contrary evidence. FP-S002510 remains excluded as a duplicate representation.

Eight batch003 paraphrased event restatements need event/cross-post links. They remain valid destination publications, but repeated schedules are not independent confirmation. Exact verbatim cross-posts already have the appropriate links.

FP-S002337, FP-S001656 and FP-S002778 remain explicit borderline review leads, not counted as definite removals. The coordinating review retains disputed FP-S002604: its explicit Jan03 exchange link and repeated precise R4 cooldown/Q1+2h15 horizon test connect to accepted FP-S002563/002567. R02 permits this clockless continuation; the scratch destination is not itself disqualifying. The reviewer's disagreement remains visible in the evidence.

## Coverage and validation

| Batch | Candidate groups | Exported trajectories | Observation decisions |
|---|---:|---:|---:|
| 001 | 50 | 50 | 680 |
| 002 | 50 | 48 | 469 |
| 003 | 50 | 49 | 375 |
| Total | 150 | 147 | 1,524 |

The review includes all candidate dispositions, not just the 1,201 currently owned observations. Four candidate groups remain deferred under the new assembly's requirement for two substantive nonduplicate contributions in two publication revisions. That threshold is an additional assembly restriction, not a retroactive rule for the original 49.

Audit artifact validation confirms 147/147 trajectory and 1,524/1,524 observation coverage, 44 literal evidence quotes, 14 proposed/discarded spans, and 54 unchanged input files, with zero errors. Source offsets/hashes and source-line references pass. No owned source-span overlaps across trajectories or full retained-span repeats in earlier same-page revisions were found. A normalization screen ignoring punctuation and whitespace likewise found none; partial-span contamination still required semantic inspection. The inherited R01–R14 file is byte-identical to the original audit rules. Cross-batch/baseline checks found no additional supported merge, and the Apr10 alias merge is already present in the final export.

The audit leaves the assembly and explorer unchanged. Findings are proposed corrections, with borderline cases distinguished from high-confidence changes. This is an internal consistency and attribution audit, not a statistical error-rate estimate or exhaustive recovery of all archive messages/clock tokens.

## Artifacts

- `reviews/batch001.md`, `reviews/batch002.md`, `reviews/batch003.md`: semantic reviews and complete trajectory coverage.
- Corresponding `.json` files: observation coverage, exact source evidence, proposed corrections and uncertainty.
- `findings.json`: 26 consolidated finding groups with coordinating resolutions (17 high-confidence, seven conservative metadata recommendations, two disputed/borderline groups).
- `observation-review.csv`: all 1,524 per-observation review records; consult coordinating resolutions in `findings.json` for disputed cases.
- `cross-batch-review.md`: baseline/alias/cross-post checks and rule interpretation.
- `integrity-check.json`, `candidate-coverage.json`, `input-manifest.json`, `review-validation.json`: provenance, complete coverage, frozen input hashes and validation of the audit artifacts.
- `check_integrity.py`, `assemble_review.py`: reproducible read-only checks and report assembly.
