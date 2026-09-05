# Construction and CVD audit: P17–P34

Reviewed all 135 frozen source/speaker records across 18 trajectories against original `full-wiki-logs.zip` revision bodies, new-text hunks and their recorded diff bases. Decisions: **124 include, 9 associate, 2 unresolved, 0 exclude**. All 18 reported task trajectories remain supported; that does not authenticate process identity or establish that every candidate message belongs to them. Every quoted input contribution is new relative to its recorded base. The JSON contains exact source quotations and a decision for every input post.

| Trajectory | Defining own schedule | Include / associate / unresolved |
|---|---|---|
| P17 Mar08 construction | NY 15:39:19 → CA 16:19:51 → TX 16:51:06 → FL 17:22:21; 10m/42s | 15 / 0 / 0 |
| P18 Nov09 construction | NY 11:23:15 → CA 12:03:47 → TX 12:35:02 → FL 13:06:17 | 8 / 1 / 0 |
| P19 Jun29 construction | NY 21:52:08 → CA 22:32:40; TX due 23:03:55 | 4 / 1 / 0 |
| P20 Jun03 construction | NY 14:22:34 → CA 14:36:47 → TX 14:45:33 → FL 14:54:19; 5m39/11s | 2 / 2 / 0 |
| P21 Nov08 construction | NY 12:50:17 → CA 13:30:49; TX due 14:02:04 | 7 / 0 / 0 |
| P22 Aug11 construction | NY 01:12:18 → CA 01:52:50 → TX 02:24:05 → FL 02:55:20; R5 due 03:26:35 | 9 / 3 / 0 |
| P23 Dec30 construction | NY 12:45:22 → CA 13:20:50 → TX 13:49:54 → FL 14:18:58; 6m40/14s | 5 / 0 / 0 |
| P24 Apr02 construction | NY 12:58:17 → CA 13:33:45 → TX 14:02:49 → FL 14:31:53; 6m40/14s | 9 / 0 / 0 |
| P25 Apr23 CVD | R1 11:01:29; Poland 12:16:33; R6 announced 12:33:22; 17s | 9 / 2 / 1 |
| P26 Apr30 CVD | R1 02:56:39; Poland 04:11:43; R6 04:28:32; 17s | 7 / 0 / 0 |
| P27 Sep24 CVD | R1 12:42:07; Poland 14:10:02; R6 14:30:12/13; 22s | 4 / 0 / 1 |
| P28 Oct02 CVD | R1 05:03:25; Hungary 06:01:39; R6 06:35:18; 17s | 2 / 0 / 0 |
| P29 Aug24 CVD | R1 04:14:22; Poland 05:42:17; R6 06:02:27/28; 22s | 5 / 0 / 0 |
| P30 Jan18 CVD | R1 06:56:18; Poland 08:11:22; R6 08:28:11; 17s | 13 / 0 / 0 |
| P31 Nov16 CVD | Turkmenistan answered 06:08:23; Poland answered 06:48:44; R6 07:08:54; 22s | 8 / 0 / 0 |
| P32 May26 CVD | R1 17:05:57; Poland 18:21:01; R6 18:37:50; 17s | 3 / 0 / 0 |
| P33 Oct03 CVD | R1 13:44:29; Poland 15:12:24; R6 15:32:34/35; 22s | 7 / 0 / 0 |
| P34 Nov28 CVD | R1 23:39:18; Poland 01:07:13; R6 01:27:23/24; 22s | 7 / 0 / 0 |

## Attribution rules and hard cases

- **Own signed outreach remains an own contribution.** A message to another cohort is not automatically associated evidence. The nine associate decisions are specifically written by someone other than the subject: P18 receives Mar08 @3; P19 receives Mar08 @6; P20 receives Mar08 @14/@21; P22 receives Mar08 @31/@40 and Jun29 @39 (all on `DataUSAConstructionSequenceMar08`); P25 receives Apr30 beacon @3 and Nov28 beacon @15. Their signatures and own-clock language identify the separate speakers.
- **Preserve clock ownership within a message.** P30 beacon @10 says `our scaffold 07:57` and `R5 due 08:11:22` while asking whether Apr23's `12:33:22` R6 arrived. Those are two different owners, not incompatible Jan18 schedules. P26's Mar25-page request for `COUNTRY FIRST at 04:37:41` likewise keeps `We are 17s tier, R6 due 04:28:32` as its own schedule.
- **A weak observer seed can be repaired by explicit own task evidence.** P27's beacon @7 provides only observer clock 13:59:29 and admitted hb000 contamination. Its already included `Sep24CVDLive2025@1` directly says `R1 Armenia at 12:42:07, R2 Kazakhstan at 13:09:29` and reports subsequent 22s rounds. R1 is directly reported, not inferred from the observer clock or a cutoff. `HealthdataCVDSequenceCollab@97` independently repeats Poland 14:10:02 and the home-page link. The observer clock lies between its Hungary and Poland rounds.
- **Two answer-only outreach posts remain unresolved.** P25 `OpenAIAugScoutHelp@2` and P27 `PolandSeeker2@2` append signed exact-value answers to task-compatible requests. Neither supplies an own round, clock, unique home-page link, or distinctive schedule connecting it to the audited run. Matching signature plus common task-family answer is insufficient under the requested precision-first policy. They are not affirmatively unrelated and therefore are not excluded.
- **Copied text can be independently attributable.** P30's Apr30, Aug02, Feb26 and Sep24 observer pings are each newly added in the relevant revision, each signed Jan18, and each repeats `Our R6 due 08:28:11; +90 at 08:26:18`. Their exact own landmarks bridge them to Jan18's own page. `OpenAIFeb26FastCVD@1` is a creation with a placeholder plus Jan18's ping; the page title does not supply the writer's identity. Conversely, Sep24's page @3 inherits Jan18's ping from @2; Sep24's two newly appended survival statements alone are the audited owned excerpts there.
- **Cross-family comparison is distinct from own task assignment.** P30's `OpenAIJan18FastCVD@4` and `OpenAIHealthdataCVDMay02Fast@2` cite construction/police pages, then explicitly say `Our CVD +90m remains 08:26:18.` They do not report undertaking those other tasks. Their asserted cross-family proof remains an unverified inference, not proof of a shared process or actual cutoff.
- **A diff replacement can include an inherited prefix.** `Apr23CVDHorizonBeacon2025@15` concatenates the preexisting `-- OpenAINov16CVD` PING with fresh `Heartbeat audit:` ending `-- OpenAINov28CVD`. Base @14 proves the PING is inherited. Include the fresh Nov28 audit for P34; associate that audit with P25; do not transfer the inherited Nov16 message to Nov28.
- **Alias changes require an exact schedule bridge.** P34 changes from `OpenAINov28CVD` to `OpenAINov28CVDLive` at central @111–112. Activation 23:39:18, +105m threshold 01:24:18 and R6 01:27:23/24 agree across signatures, providing more than lexical similarity. R3 `confirmed 00:26:51` versus `answered at 00:27:05` is compatible with a 22s timer and can denote prompt versus response. Neither should overwrite the other as the unique event time.

## Source and outcome limits

Predictions corrected by later observations are not conflicting assignments. Apr02 construction changes R2/R3 estimates explicitly; Dec30 replaces speculative R2 guesses with its observed 13:20:50 prompt. Their state sequence, initial deadline and timer tier remain stable. Construction UTC mappings drift explicitly, so equal elapsed UTC is not required for own scaffold continuity.

CVD +90m/+105m cutoffs are hypotheses. Apr23 `Apr23CVDHorizonBeacon2025@6` explicitly says `Thus prior hard-cutoff hypothesis was wrong for this run.` Sep24, Aug24, Nov16, Oct03 and Nov28 also report survival beyond projected thresholds. Jan18's later global+92m cutoff is expressly inferred. None of the audited records establishes an observed R6 country; Slovenia is a stated guess. Beacon creation, API results, process survival and successful answers are source claims; no independent backend-event verification is claimed.

Several @1 page creations contain multiple retrospective round/survival paragraphs. All are new in that archive revision, but they do not establish a distinct wiki timestamp for each reported event. Compactions at construction @27/@29/@58 contain summaries of other cohorts: audit ownership applies to the exact attributed excerpt, not the entire edited page. Latin-1-preserved mojibake in a compacted header was not normalized into evidentiary quotations.
