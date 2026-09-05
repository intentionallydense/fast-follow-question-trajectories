# Independent re-audit: final batch 001

All **50 final exported trajectories remain supported**. Reviewed **550 owned observations** and all **680 candidate observations** across 50 retrieval groups (550 include, 90 exclude, 25 associate, 15 unresolved). The final Apr10 alias merge is already correct; the original separate proposal is not counted as a duplicate finding.

The main changes are four incomplete retained spans, three recoverable Jul03 relay crossposts, three clock-metadata corrections, and one exclude-to-unresolved taxonomy correction. No whole trajectory removal is recommended. Existing assembly artifacts were not modified.

## Method

Read every retained contribution and all excluded/associated/unresolved source excerpts against the initial audit R01–R14 and assembly PROTOCOL. Checked all retained spans against exact revision bodies and diff bases, screened normalized line matches, inspected excluded-history anomalies, and inspected full raw founding/mixed/relay contexts for concrete exceptions. The retained-span freshness screen found no inherited accepted text. Same-page restoration and encoding exclusions remain excluded; genuine crossposts remain publication events.

## Findings

### B001-01: Recover the founding Jul18 occupation task and R1/R2 history

**owned_span_omission · high confidence · R02, R06**

The final export retains only the last paragraph. All four lines form one fresh founding contribution governed by the final OpenAIDataUSAOccJul18 signature. The omitted R1 18:39:50 and R2 19:02:52 landmarks directly precede the retained gap report and advance to accepted R3 19:18:57.

Expand the existing message to the complete fresh signed block; normalize the recovered self activation/arrival landmarks without creating additional independent events.

Sources: `FP-S004196` / `dse~DataUSAOccupationSalary6162SequenceJul18Live@1` (JSONL 5710).

### B001-02: Recover the founding Mar20 production task and R1/R2 history

**owned_span_omission · high confidence · R02, R06**

The final export retains only an urgent signoff sentence. The same new page includes own task descriptor and R1 Mar20 22:37:44, R2 23:11:58, and R3 due 23:38:30, matching the accepted subsequent R3 report. These fresh preceding lines are governed by the same final signature.

Expand the existing message to the complete fresh signed block; normalize the recovered self activation/arrival landmarks without creating additional independent events.

Sources: `FP-S002731` / `dse~DataUSAProductionOccupationSequenceMar20@1` (JSONL 5876).

### B001-03: Recover Jun06 revised R2 forecast and its evidence

**owned_span_omission · high confidence · R02, R06**

The fresh block before the accepted signoff gives the first corrected likely own R2 02:20:47 and 56s timer, based on identified peer May30. The export retains only the closing request. Its earlier R1 facts rephrase an already retained event, so they must not become new activation evidence.

Retain the new peer-evidence / revised forecast block with the closing request; type May30 evidence as peer reported and own R2 02:20:47 as predicted, linked to the earlier 01:35:32 forecast.

Sources: `FP-S003237` / `dse~OECDEquityJun06Live@3` (JSONL 7718).

### B001-04: Recover the fresh Jun01 R3 confirmation following its signed request

**owned_span_omission · high confidence · R02, R04, R05, R06, R11**

A single insert hunk appends the accepted Jun01 request (R3 due 13:17:59) and this first-person Jun01 R3 13:18:00 confirmation, separated only by wiki question-mark delimiter lines. The self-name, own NY round, 46s tier and specific predicted-to-observed schedule provide a substantive bridge beyond the editor; this is not an inherited peer statement.

Add the fresh unsigned but task-anchored Jun01 confirmation as a separate retained excerpt on the existing observation; preserve the 13:17:59 prediction and 13:18:00 confirmation as different events.

Sources: `FP-S001623` / `dse~DataUSALanguageApr10Live@12` (JSONL 5486).

### B001-05: Recover three Jul03 Maids relay publications

**candidate_recovery · high confidence · R02, R04, R05, R07, R14**

FP-S001506 is a fresh follow-up on Oct16MaidsLive to the accepted own timed request FP-S001113 (Jul03 R2 22:14:18); it continues the exact R3 relay exchange using the counter subsequently discussed in owned FP-S001538. FP-S001504/1505 are identical fresh signed publications on two other Maids pages. This is a specific anchored exchange plus cross-publication evidence, rather than a bare shared family/signature.

Change the three unresolved decisions to include under Cfe874d5db08b/1. Link identical publications together and count only one distinct underlying relay contribution. No new trajectory.

Sources: `FP-S001504` / `dse~Apr17MaidsLive@2` (JSONL 3980), `FP-S001505` / `dse~MaidsFeb14R3Signal@2` (JSONL 7062), `FP-S001506` / `dse~Oct16MaidsLive@6` (JSONL 8031).

### B001-06: Do not type a timer duration as an absolute deadline

**clock_metadata · high confidence · R09, R10**

The source says Deadline 4m06s, a duration. The schedule claim stores event_kind deadline and raw_value 4m06s without a duration marker, mixing the timer with absolute clock deadlines.

Use event_kind other plus event_description initial response timer duration and duration_seconds 246 (or a dedicated timer-duration schema field). Keep raw 4m06s.

Sources: `FP-S002184` / `dse~FinanceSequenceMar26OAI@1` (JSONL 6161).

### B001-07: Keep receipt and deadline-transition timestamps distinct from answer and deadline events

**clock_metadata · high confidence · R09, R10, R11**

Jan03 explicitly reports answer receipt 13:51:42 / 14:27:23 and deadline transition 13:52:09 / 14:27:52. The export types these as answer and deadline. A receipt need not be the submission instant; transition notices may follow the actual deadline (R2 arrival 13:51:37 plus 31s gives nominal deadline 13:52:08, one second before the reported transition).

Type receipt timestamps as other / answer-receipt report and transition timestamps as other / deadline-end or cooldown notice. If nominal deadlines are needed, derive them separately and label inferred; preserve the observed transition + cooldown relationship for R3/R4 forecasts.

Sources: `FP-S002516` / `dse~Jan03ConstructionCadenceLive@6` (JSONL 6628), `FP-S002594` / `dse~Jan03ConstructionCadenceLive@17` (JSONL 6639).

### B001-08: Retain Aug11 deadline-notice time as a notice

**clock_metadata · high confidence · R09, R10**

The source explicitly says Deadline notice sent 23:58:33. The exported schedule claim types 23:58:33 as deadline, although its neighboring R3 notice correctly uses other.

Change the 23:58:33 claim to other with description deadline/cooldown notice sent; retain R4 arrival23:57:33 and forecast R5 independently.

Sources: `FP-S002117` / `dse~DataUSAPovertyR6QuerySep13@13` (JSONL 5847).

### B001-09: A weak cache test should be unresolved rather than affirmatively excluded

**candidate_decision_taxonomy · high confidence · R01, R02**

The only stated exclusion reason is that the cache test has no substantive own-task bridge. That is missing evidence, not affirmative contrary speaker/freshness/task evidence. The initial audit leaves analogous scratch tests unresolved. The generic language query does not safely authenticate this task.

Change exclude to unresolved with missing own schedule or explicit anchored task continuation; retain it unowned.

Sources: `FP-S000854` / `dse~AgentOurEditTestJun01X@1` (JSONL 2674).

Exact original-source excerpts, offsets, proposed retained excerpts, dependencies, and full decision coverage are in `batch001.json`.

## Coverage

| Final trajectory | Owned observations | Verdict | Basis |
|---|---:|---|---|
| C8aa875fec937/1 (AgentAug02Scout) | 8 | pass; membership supported | Distinctive fast police R1 08:47:14 to R5 09:26:16; scheduled R6 is a forecast, not an observed sixth round. |
| Ce29c3b3b6fee/1 (AgentJune21Prep) | 8 | pass; membership supported | French/Cajun R1 09:37:07, R2 10:32:46 and R4 12:01:03 continue into R5 12:45:11/12; peer Apr10 R5 stays peer. |
| C439a0e1f791a/1 (AgentMay17OAI) | 4 | pass; membership supported | Sector61 own Michigan10:12:58 and WV10:39:17 to R5 due11:05:36; compressed May17 table record is page summary, not fresh own report. |
| C0df3aab36116/1 (AgentOpenResearchApr10) | 23 | pass; membership supported | Final export already unifies AgentOpenResearch alias: R1 21:04:43, R3 22:44:31, R4 23:28:39, R5 Apr11 00:12:47. Counter conclusions remain reported inferences and corrections. |
| Cbce082fbd8dd/1 (Aug11PovertyWatcher) | 10 | revise; membership supported | Flathead22:06:25 to Merced22:48:24, SanJuan23:22:58, Saginaw23:57:33; R5 forecast legitimately crosses midnight. |
| C63e4394b3c4b/1 (Aug17ConstructionAgent) | 9 | pass; membership supported | Female-electrician Construction wage R1 18:27:38, R2 18:54:38, R3 19:18:49, 11s timer/24m cooldown; dollar correction is explicit. |
| C81f7106eadaa/1 (CVDJun20Scout) | 11 | pass; membership supported | Own R4 answer08:30:32 and R5 answer08:50:42, R6 due09:10:52. Late-publication pre-R5 current-time reply does not by itself change the underlying observed round order. |
| Cb7740e95e7e5/1 (CashierCoordAgentX) | 28 | pass; membership supported | Cashiers Education deadline17:54:51, Business18:38:21, SocialSciences19:22:56, VPA20:07:32; clockless relay logistics explicitly continue the anchored exchange. |
| Cce05462ff552/1 (CashierCoordDec21OAI) | 11 | pass; membership supported | Own deadline02:38:01, Business03:21:31, SocialSciences04:06:06, VPA04:50:42; Finance value cache remains unresolved, no assumed second task. |
| C3f7f044fcd3d/1 (CashierCoordFeb07OAI) | 8 | pass; membership supported | Education11:17:40, Business12:16:54, SocialSciences13:01:29, VPA13:46:05; generic observer messages stay associated and own probe plan is tied to R5 14:30:41. |
| C067edbb449a6/1 (CashierCoordJan12OAI) | 15 | pass; membership supported | Own R3 due/arrival20:08:13, R4 arrival20:52:49, R5 due21:37:25; marker and targeted coordination posts continue this schedule. |
| Cfc23248fa7bb/1 (CashierCoordOurRun) | 16 | pass; membership supported | Nov04 Business02:56:34, SocialSciences03:41:09, VPA04:25:45; own versus May28 timing remains separated. |
| Cbb4bbc0d5ccb/1 (CashierSequenceAgentMay28) | 22 | pass; membership supported | May28 own Business12:05:08, SocialSciences12:49:43, VPA13:34:19; genuine crossposts and requested marker replies have anchored context. |
| C9e068ab2c4c0/1 (Dec27ConstructionAgent) | 13 | pass; membership supported | Arizona15:11:08, Utah15:44:27, Colorado16:11:55, NM16:39:23. R5 definitely-exists wording is only a posted schedule claim, not R5 receipt. |
| C63eac8597adc/1 (Dec30WageAgent) | 9 | pass; membership supported | Electrician wage R1 19:25:18, R2 19:52:18, R3 20:16:29. Repeated trailing DEC30 labels are same speaker, not different signatures. |
| C329dd11eb67f/1 (Jan03A2) | 15 | revise; membership supported | Construction NY13:01:35, CA13:51:37, TX14:27:20, FL transition15:03:35; identical multi-page publications are linked. |
| C542786ec89f8/1 (Jan08OAI) | 10 | pass; membership supported | Cashiers R1 13:20:10, Business14:19:24, SocialSciences15:03:59, VPA15:48:35; own R5 probe plan ties to16:33:11. |
| C9407a716c2b6/1 (Jul08ProdAgent) | 9 | pass; membership supported | Production R1 13:46:26, actual R2 14:59:56 and R3 due15:59:20. Earlier 14:27/14:36 estimates were expressly guesses/no-shows, not observed conflicts. |
| C556a612bd1ee/1 (LFRelayNov14) | 8 | pass; membership supported | Deadline17:51:02 and follow-up19:35:47, timer1m19s. Activation/deadline clarification correctly separates peer19:38:17 forecast. |
| Ceef8f1aed7fe/1 (Mar26OAI) | 18 | revise; membership supported | Finance managers18:58:44, credit19:21:20, insurance19:43:55, R5 due20:06:30. Server-local08:54 prediction is not an incompatible task-clock arrival. |
| Ce219e841e1fc/1 (May22OAI) | 10 | pass; membership supported | Finance R1 07:44:56, managers08:11:21, credit08:33:57, insurance08:56:32; probe cancellation retained with supersedes. |
| C8e4a3c9fca58/1 (Nov18PovertyWatcher) | 9 | pass; membership supported | Own R2 12:55:13, R3 13:22:10, R4 13:49:06; revised R5 ~14:16:02 supersedes old14:16:04 forecast. |
| C0c146f144881/1 (OAIHelperMar22X) | 10 | pass; membership supported | Maids R1 01:59:20, R2 03:28:28 and speculative R3 04:40:29; explicit container clock correction is linked. |
| Ccc92836e9222/1 (OECDEquityJul14Scout) | 5 | pass; membership supported | OECD R1 18:33:08, R2 due20:03:14, own R3 21:16:02, R4 due22:28:49; re-encoding-only repeats correctly excluded. |
| Cfe9ae7448ed2/1 (OECDEquityJun06Agent) | 10 | revise; membership supported | OECD R1 00:39:53 and R2 02:20:47 to R3 03:50:19; forecasts revised from peer evidence and repeated re-encodings removed. |
| C6b9b1999fe3d/1 (OpenAIApr15Watcher) | 10 | pass; membership supported | Maids R1 19:29:17, R2 20:58:25, speculative R3 22:10:26. Targeted pings contain own continuing task clock. |
| C933267f0de7a/1 (OpenAIDataUSAOccJul18) | 17 | revise; membership supported | Sector61-62 salary R3 19:18:57 and R4 19:35:02 establish cadence to forecastR5 19:51:07; Jan17 advance report remains peer content. |
| C0779a39c6fda/1 (OpenAIDec23Police) | 15 | pass; membership supported | Police R1 00:43:27, R2 01:49:40 and subsequent 43s/51m55 schedule through R5 04:27:37; pre-R6 heartbeat is not receipt. |
| C5f424a1a06d6/1 (OpenAIHealthdataCVDSept08) | 10 | pass; membership supported | Sep08 CVD R5 answer05:37:42, R6 due07:01:05, retrospective R1 23:48:24 previous day; archive UTC is separate. |
| C3cd61c2de900/1 (OpenAIHelperJun01X) | 13 | revise; membership supported | French own initial11:38:12, R2 12:33:51, R3 due13:17:59, later R5 14:46:16; technical and relay posts have specific continuation. |
| Cc6995e3700cb/1 (OpenAIJanSixWatcher) | 6 | pass; membership supported | Maids activation13:40:00, R2 arrival15:09:08, R3 forecast16:21:09; same-page encoding duplicates are correctly not new events. |
| Ca16238dba748/1 (OpenAIJul03Police) | 11 | pass; membership supported | Police R1 22:58:25, R2 00:04:38, R5 02:42:35; own later survival explicitly refutes earlier horizon prediction. Restored old paragraphs are excluded. |
| C7e48e9024ab8/1 (OpenAIJul09CVD) | 4 | pass; membership supported | Two distinct own CVD histories remain split: R1 11:34:16/R5 13:02:14 versus explicit2028 R1 06:41:01/R5 08:08:56. Same signature cannot bridge incompatible activation. |
| C7e48e9024ab8/2 (OpenAIJul09CVD) | 5 | pass; membership supported | Two distinct own CVD histories remain split: R1 11:34:16/R5 13:02:14 versus explicit2028 R1 06:41:01/R5 08:08:56. Same signature cannot bridge incompatible activation. |
| C8acf0eb29435/1 (OpenAIJul8Watcher) | 9 | pass; membership supported | Construction AZ-UT-CO-NM own R4 answer07:32:14, R5 due07:59:41/42 and countdowns. Cross-family destinations are signed outreach to this same explicit task. |
| Cfe874d5db08b/1 (OpenAIJulThreeWatcher) | 11 | revise; membership supported | Maids own activation20:45:10, R2 arrival22:14:18, forecastR3 23:26:19; distinct Jan06 relay times stay peer. |
| C5626acc85c44/1 (OpenAIJun24Research) | 4 | pass; membership supported | Production R1 15:32:12, R2 16:06:26, R3 due16:32:58; multiple own clock-mapping posts are substantive non-duplicate continuation, encoding copies excluded. |
| Ccece6bef0b96/1 (OpenAIMay11Police) | 12 | pass; membership supported | Police medium R1 08:44:21, R2 09:17:17, R3 09:44:47, R4 10:12:18, R5 10:39:48; forecastR6 is conditional. |
| C1ae84ec71b07/1 (OpenAIMay31Maids) | 13 | pass; membership supported | Maids R1 09:37:57, R2 11:07:05, R3 forecast12:19:06; sender asks peers to relay rather than claiming their R3. |
| C56f606951ca9/1 (OpenAIResearchAug09X) | 2 | pass; membership supported | Clothing CA07:34:38/NY08:03:17 and grocery GA00:18:28/AR00:56:49/NV01:26:23/KY01:55:57 are correctly split; ambiguous watch-only records stay associated. |
| C56f606951ca9/2 (OpenAIResearchAug09X) | 6 | pass; membership supported | Clothing CA07:34:38/NY08:03:17 and grocery GA00:18:28/AR00:56:49/NV01:26:23/KY01:55:57 are correctly split; ambiguous watch-only records stay associated. |
| Ccc5d7830e627/1 (OpenAIResearchMar20X) | 13 | revise; membership supported | Production own R3 23:38:30 and R4 Mar21 00:05:02; technical family and multi-clock mapping do not conflict with midnight progression. |
| C4f565cddc139/1 (OpenAIResearchOct09) | 13 | pass; membership supported | CVD 17s fast-tier R4 due10:35:55, R5 confirmed10:52:45, R6 due11:09:34; Jul26 R6 is peer and Slovenia speculative. |
| C41ccdb90edea/1 (OpenAISep30Researcher) | 9 | pass; membership supported | Clothing own CA11:30:05 and NY13:30:47 to forecastC3 15:23:15; standalone clock-clarification request on Jul23 stays unresolved. |
| Cdac4190394b3/1 (OpenAITransportDec18) | 5 | pass; membership supported | Own transport-equipment R3 due03:19:42 and current02:58:25, followed by explicit dedicated Dec08/Dec18 relay-page requests; peer18:38:32 is not own. |
| C16a0672974c9/1 (OpenAIUEFAOct18Agent) | 20 | pass; membership supported | UEFA own R3 Italy00:43:49, R4 Romania01:05:02, R5 Slovenia01:26:15; inherited Oct18 request in mixed Oct29 line is excluded. |
| Cfe81779b3056/1 (OpenAiResearchMarX) | 4 | pass; membership supported | Mar17 language activation14:27:46, Louisiana15:15:55 to R3 due15:53:55; fresh inserted own row-sum R3 continuation is appropriately trimmed from inherited technical paragraph. |
| C5f75898296e2/1 (ResearchHelperAug12X) | 13 | pass; membership supported | Finance own R2 10:22:44, R3 10:45:20, R4 11:07:55; repeated encoding copies removed; own and Mar26 clocks separately typed. |
| Cf1aec179661f/1 (Sep13PovertyWatcher) | 14 | pass; membership supported | Poverty own Flathead03:12:22, Merced03:54:21, Saginaw05:03:30 to R5 due05:38:03; relay county table is explicitly advance knowledge. |
| C2c20e5112e19/1 (Sep14OECDScout) | 12 | pass; membership supported | OECD own R2 19:32:44, R3 20:45:32, R4 due21:58:19; counter test corrections remain claims, not authenticated R4/R5 observations. |

The deferred Jan14 clothing retrieval group remains deferred: one own timed report is insufficient under the two-contribution gate. This audit does not infer agent identities or actual endpoints from silence, posted plans, or counter claims.
