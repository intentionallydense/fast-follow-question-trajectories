# Independent re-audit: batch002

Reviewed all 50 candidates, 48 exported trajectories and 469 observation decisions: 371 include, 58 exclude, 27 associate, 13 unresolved.

All 48 task groupings remain supported. One owned span needs trimming; seven further findings are conservative clock-metadata review recommendations only (not identity failures). Both deferred candidates remain below the assembly gate. No supported whole-trajectory merge, split or removal is recommended.

## Findings

### B002-F01 — C78a3a6b4eb2c/1 (span_membership)

The exported owned span starts with the generic wiki new-page placeholder. PROTOCOL explicitly forbids retaining inherited wiki placeholders when expanding signoff context. This is not part of the signed task report.

Evidence: FP-S000358; R04, R06.

Keep inclusion but remove the leading "Beschreibe hier die neue Seite.\n\n"; recompute span offsets/hash. No trajectory removal.

### B002-F02 — C53503371b926/1 (clock_metadata)

R1 05:56:49 and R2 06:52:28 are both typed prompt_arrival, but selected source gives bare round history and a value answer, without an arrival clause or separately timed answer.

Evidence: FP-S001286; R09, R10.

Use event_kind=other for both reported history times, with arrival-versus-answer unspecified, unless a stronger exact source is attached.

### B002-F03 — C481158764532/1 (clock_metadata)

R4 23:52:39 is typed prompt_arrival though source says CONFIRMED at ... answered exact and supplies no separately timed answer. Same timestamp confirmation on own page does not independently disambiguate event type.

Evidence: FP-S003798; R09, R10, R11.

Retain owned message; type R4 as other/reported round confirmation, or attach an explicit arrival source. Preserve R5 nominal 00:12:49 and likely :50 as alternatives.

### B002-F04 — C7d0bc6963ac9/1 (clock_metadata)

CA00:11:15 and NY00:39:54 are typed prompt_arrival although source is bare CA time and NY confirmed time with an untimed answer.

Evidence: FP-S000861; R09, R10.

Retain membership and raw clock reports; type as other unless explicit prompt-arrival evidence is attached. The +28m39 relation supports continuity, not precise event classification.

### B002-F05 — Cbe0f163b3df4/1 (clock_metadata)

R5 CONFIRMED at task05:21:54 is typed prompt_arrival. The source states a pre-final signal but gives no explicit prompt-time versus signal/confirmation-time distinction.

Evidence: FP-S001999; R09, R10.

Retain owned contribution; use other/reported round confirmation (pre-final) rather than exact prompt_arrival.

### B002-F06 — C0ae74a6ef1ad/1 (clock_metadata)

The normalized R3 prompt_arrival01:08:43 comes from "URGENT May01 R3: Alabama at ...; answered ..." without an explicit arrival clause or separately timed answer.

Evidence: FP-S004112; R09, R10.

Use other/reported round history, or supply explicit arrival evidence. Do not split the trajectory: forecast01:08:42 and later history01:08:43 are different claim statuses.

### B002-F07 — C133f9dcdecfc/1 (clock_metadata)

R1 20:06:23 is normalized as prompt_arrival from a bare R1 clock; source does not explicitly label arrival.

Evidence: FP-S004204; R09, R10.

Use other/reported initial round time unless the fuller source explicitly identifies prompt arrival. Keep R2 actual arrival21:12:06 as prompt_arrival.

### B002-F08 — Cb65c20c9ffd9/1 (clock_metadata)

The ~08:24:39 value estimates the time of an unidentified external counter hit in Mar31 scaffold units, but owner=self presents it among owned schedule events. The author explicitly asks whether actual R5, accident, test or crawler caused it.

Evidence: FP-S004191; R04, R09, R13.

Set owner=uncertain and describe event as inferred external counter creation converted to Mar31 scaffold; keep status=inferred and do not treat it as an owned task event.

## Coverage

| Candidate | Name | Verdict | Reason |
|---|---|---|---|
| C5e9d369f2fe0 | GroceryAgentJul17X | supported | GA 16:01:10 to observed AR 16:38:25 and KY 17:48:53; relay backlinks retain ownership. Same-revision redundant paragraph is already represented, not an additional publication. |
| C834ff13c3122 | Jan14PovertyWatcher | supported | Flathead 23:18:45 to Merced 00:00:44 and San Juan 00:35:18 to Saginaw 01:09:53; midnight wrap and forecasts are coherent. |
| C8cdc4c0265d4 | Jul30OECDHelper | supported | R1 deadline 04:22:30 links changing R2 hypotheses to actual 05:51:06. Negative monitoring and corrected predictions are not contradictory observed arrivals. |
| Cb1a10d1ad2a3 | LanguageHelperOct23 | supported | Louisiana 04:34:59 and NY 05:19:14 lead to NH prompt 06:03:30; Oct23 and Sep23 clocks remain separate. Revision19 restores old text and is correctly excluded. |
| C7a90b9e58e15 | March13OECDHelper | supported | R1 03:03:24 and deadline03:15:42 lead through unsuccessful forecasts to actual Hungary04:44:18 and Poland06:13:50. Technical exchange explicitly continues R3 precision work. |
| C0ae74a6ef1ad | May01PovertyStateScout | supported | Louisiana23:01:17, Mississippi00:07:39 and Alabama01:08:43 link to Georgia02:09:48; earlier due predictions are not observed conflicts. |
| Ca1e5a0b1e91b | OAI7C97Dec15 | supported | R4 due11:18:47 becomes arrival11:18:48 and R5 answer12:42:15; timing pings and horizon hypothesis continue the anchored CVD exchange. |
| Cce8d86029542 | OAIEquityDec02 | supported | Czech04:59:08/deadline05:11:26 anchors revised Hungary06:40:02. Restoration/re-encoding excluded; revision3 fresh tail is properly trimmed. Precision and OCT26 counter-provenance replies continue specific anchored work. |
| C481158764532 | OAIJan14CVD | supported | R1 activation22:44:55, R3 answer23:32:28, R4 confirmation23:52:39 and survival00:29:57 link one run; midnight and one-second predictions are bounded. |
| Ca3a658a192d1 | OpenAIDec07Police | supported | R1 05:13:17 links actual R2 05:46:13 and R3 06:13:43 to later R4/R5 history. Literal shell date text is inert, not a clock. |
| Cec8b448615db | OpenAIHealthdataCVDFeb05 | supported | R5 prediction12:02:39 becomes reported answer with explicit R6due13:26:04; advancing authoritative countdowns establish own-task continuity. |
| Cbe12eb38b0eb | OpenAIHealthdataCVDNov01 | supported | Owned R5due12:54:18 becomes explicit arrival and R6due14:17:43. Conflicting02:53:55 record and clockless potentially conflicting ping remain unassigned. |
| Cf5f9c384af2d | OpenAIMay09Police | supported | Activation09:21:21 and R2due09:54:17 become confirmed R2. Hub backlinks and same-medium-tier outreach connect peer questions; inherited collab text excluded. |
| C295b1139efd8 | OpenAIResearchSep23Lang | supported | Own initial21:15:03, R2 22:05:33 and R3 22:49:48 lead to explicit NH23:34:04 and R5due00:18:20. Restoration excluded. |
| C686215bd19b4 | OpenAIResearcherAug27X | deferred_gate_upheld | Defer: two timed publications restate the same CA18:59:07/NY19:58:06 state; cross-post alone fails the two substantive contributions gate. Peer probes provide no independent own-task continuation. |
| Ccd3cd82a83cd | OpenAIResearcherNov26 | supported | Flathead19:27:59 then Merced19:57:31, SanJuan20:24:28 and Saginaw20:51:24 establish continuity. RNG follow-up continues anchored experiment; changing forecasts are not comparable observed conflicts. |
| C55d3046e24ac | OurMaidsCoordOct11 | supported | Female2015 05:06:44 and own Male2016 05:47:07 connect Oct11 relay. Jul17 14:09:47/18m04 own-task report remains unassigned rather than merged. |
| Ce8469158a553 | SectorAgentNov27OAI | supported | MI11:40:55 to WVanswer11:56:50 and R5due12:12:43/44; scratch/status tests are not substantive task membership anchors. |
| Caa2f88208b72 | Sep18ConstructionAgent | supported | Female-electricians2014/3m tier continues to2015 19:55:58 and2016 20:20:09. Dedicated-task-page outreach is valid even on other task families. |
| C57c992ff4cb6 | Sep19OECDAgent | supported | Deadline10:57:23 and Hungary12:08:50 bridge Poland13:21:38 and R4due14:34:25. Precision corrections continue specific investigation; peer-only beacon pings stay separate. |
| C7d0bc6963ac9 | Sep26ClothingAgent | supported | CA00:11:15 and NY00:39:54 anchor advancing own C3 countdowns01:05:52/01:08:33. Peer Jan01 probe stays separate. |
| C67d45adaeab3 | Sep26WageAgent | supported | Own construction R2answer04:35:51, R3due05:00:02 and success05:00:02 establish continuation; cross-family poverty outreach explicitly identifies the construction task and cadence. |
| C2aa7e6be4cc7 | Apr17MaidsWatcher | supported | Female2015 activation19:05:33 and Male2016 actual20:34:41 connect own21:46:42 candidate and advancing clock reports. Jan06 investigation is explicit in own hub updates. |
| Cbe0f163b3df4 | CashierCoordMar20OAI | supported | Education02:08:53, Business03:08:07 and SocialSciences03:52:42 anchor R5due/confirmation05:21:54; acceleration change is documented and no fixed UTC offset assumed. |
| C0ad979614657 | GroceryProbeJul09 | supported | GA21:33:06, AR22:11:27 and NV22:41:01 anchor Jul09. Apr20 relay is explicitly peer evidence; later own-hub report links targeted Apr20 monitoring. |
| Cf30cf8257544 | Jan02CVDScout | deferred_gate_upheld | Defer: all seven substantive history/heartbeat/survival paragraphs are within one archived publication revision; cannot satisfy two-distinct-publication gate. |
| C53503371b926 | LanguageRunnerNov22 | supported | Louisiana06:52:28 and NYdue07:36:36 bridge ownNHdue08:20:44 with advancing task clocks. Shared signal response explicitly reports Sep01 California, not own R5. |
| Cac5232b0878f | LanguageWatcherNov12 | supported | LA10:14:27 and NYconfirmation10:52:27 link NH11:30:28/R5due12:08:28. Specific CA counter inquiry and shared presignal/backup exchange continue this run; generic UI replication remains associated. |
| C6483634209b2 | Nov28OECDAgent | supported | R1deadline00:43:39 links negative R2 tests to observed02:12:15 and Poland03:41:47; predictions are not confused with actuals. |
| Cf575d4724a5f | OAIResearchDec13FP | supported | Croatia06:01:22/deadline06:12:07 leads to Albania07:30:45/Cyprus08:50:14. RNG methodology explicitly follows signed anchored experiment; inherited re-encodings excluded. |
| Cf5f1ec8813e7 | OECDEquityApr19Agent | supported | R1deadline18:39:11 and later full founding history link Hungary20:07:47. Precision replication and peer inquiry continue own R2 report. R2 cross-post is a separate publication, not independent identity evidence. |
| C8042105c2ca9 | OECDEquityMar15Agent | supported | R1deadline17:27:13 leads through predictions to actualHungary18:55:49 and Poland20:25:21; competing forecasts do not imply multiple tasks. |
| Cb65c20c9ffd9 | OECDEquityMar31Team | supported | Hungary07:34:30/transition07:35:02 predicts Poland08:10:46, later observed and leading toR4due08:47:02. Mixed adjacent peer requests continue own timing exchange. |
| Cb2584db93dbb | Oct18Helper | supported | AZ/UT construction task predicts Colorado10:57:49, confirms10:57:50, then NM11:25:18. Explicit cooldown supersedes earlier four-corners termination hypothesis. |
| C133f9dcdecfc | OpenAIApr30SchoolScout | supported | R1time20:06:23/deadline20:14:35 connects R2due/arrival21:12:06 and next22:10:10. API-value correction belongs to same anchored task exchange. |
| Ce0f796c8acfe | OpenAIDec17ConstructionX | supported | NY12:40:35/CA13:21:07 connect Texas13:52:22 and Florida14:23:37; claimed fixed horizon is retained as inference, not proven endpoint. |
| C45da12196474 | OpenAIHealthdataCVDSept27 | supported | Polandanswer05:46:29 and explicit R6due07:09:51 link advancing countdown and specific Nov21/Apr04 monitoring. |
| C0f65c40a17a2 | OpenAIMar09Scout | supported | R1 17:18:26, R4answer18:26:10 and R5answer18:46:21 link dedicated heartbeat and successive survival checks. No actual termination inferred. |
| Cb18543a4eeb7 | OpenAIOct22CVD | supported | R1 08:11:46/R4answer09:19:30 connects R5 and survival09:58:31. Mixed founding line is correctly split; incompatible Apr30-page own04:27:31/90m52 remains unresolved. |
| C883248ff7bcd | OpenAIResearchAug21X | supported | Production2013 R1 15:06:00 and R2due16:58:45 connect actual2016 and2019 18:34:59. Peer Jul08 clocks remain separate. |
| C311eb2077f01 | OpenAIResearchJan02 | supported | Business01:06:13 leads toEducation01:21:13, SocialSciences01:33:24, Arts01:45:35. Revision2 correctly trimmed to fresh progression. Counter accident time is writing/activity after round history, not a backwards prompt. |
| Cded8d04dd8da | OpenAIResearchOct25X | supported | Activation15:16:27/R5answer16:31:31/R6due16:48:20 link explicit heartbeat startup and survival reports. Predicted endpoint remains unverified. |
| Cd396b3dcd425 | OpenAIResearchSep22 | supported | R1 00:56:23/R5answer02:24:18/R6due02:44:28 link several same-revision survival paragraphs to the distinct earlier collab publication; threshold exceeded is not observed R6. |
| Cf4b843ad9b80 | OpenAIUEFAOct29Scout | supported | Italy13:08:32 and Romania13:29:45 connect explicitR6due14:12:11 and countdowns. Mar16 R5 relay is Oct29 publication with peer observation ownership; mixed Oct18 clause excluded. |
| C78a3a6b4eb2c | ResearchAgentAug01 | supported_with_span_trim | CA17:38:33 and NY18:07:12 establish own run with revised C3 forecasts and targeted anchored peer probes; founding page retains a wiki placeholder requiring trim. |
| C4bfc80afe89b | AgentFrenchPrepXQ29 | supported | NHdue/confirmation01:04:08 connects R5due01:42:08 and advancing01:29:02 countdown; compact relay backlinks and counter-noise continuation are substantive. |
| Cd1b6cde79b3c | AgentJune25OAI | supported | MA04:45:55/CT05:14:01 connect ownWVanswer06:06:41/R5due06:33:00. Compacted multi-speaker table is a restatement rather than new owned progression. |
| Cc4b88a3e2a9c | AgentOpenAIJun28X | supported | CA15:39:48 links NYforecast/actual16:08:27 and C3alternatives16:34:25/16:37:06; duplicate mapping excluded. |
| C30dde3d5edc3 | Aug02Precision | supported | Aug02 R2 20:52:29 links precision request/correction to actualHungary and Poland22:22:01. Apr11 terminal interpretation remains separately associated. |
| C70fb2cbab4da | CashierCoordJul05OAI | supported | Education05:13:53 and Businessdue/actual06:13:07 connect R3due06:57:42 and explicit global-versus-task activation distinction. Peer termination experiments remain associated. |

## Source checks and limits

Every selected source span exists in the archive and lies in the recorded changed hunks; none is an exact whole-span repeat in its immediate diff base. That check does not by itself prove speaker ownership or substantive freshness. Raw comparisons confirm the Jan02 deferred group has only one publication revision, the Aug27 deferred pair repeats one task state across pages, and the Nov01/Oct11/Oct22 competing histories are correctly left unassigned. Excluded same-page restorations, repeated encodings, scratch tests and compacted summaries were reviewed as retrieval observations, not new task events.

The seven clock findings retain task membership. They prevent exact arrival or event ownership claims stronger than the cited language. These are reports made in posts, not independently verified harness telemetry. Detailed per-observation coverage and source references are in batch002.json.
