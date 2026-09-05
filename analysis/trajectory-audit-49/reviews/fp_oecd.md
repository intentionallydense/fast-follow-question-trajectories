# Family planning and OECD audit: P35–P49

Reviewed all 95 frozen input post records for 15 trajectories against original `full-wiki-logs.zip` revision bodies and their declared diff bases. Result: **87 include, 6 associate, 2 unresolved**; 14 supported reported trajectories and one provisional trajectory (P43). No complete post requires exclusion. One included record requires an explicit content trim. These verdicts concern reported tasks, not authenticated persistent processes.

| Trajectory | Decision summary | Distinguishing schedule |
|---|---|---|
| P35 Mar31 FP | 2 include | R1 07:25:51; R2 Albania 08:55:14; R3 Cyprus 10:14:43; 51s follow-ups |
| P36 Sep05 FP | 15 include, 1 associate | R1 08:34:20; R2 09:58:30; R3 11:17:20; R4 due 12:36:10; 39s |
| P37 Nov28 FP | 1 include | R1 01:44:20; 5m59 initial; R2 forecast 03:08:57 |
| P38 Nov27 FP | 4 include, 1 associate | R2 05:01:00; R3 06:19:50; R4 forecast 07:38:40; 39s |
| P39 Jul20 FP | 6 include, 1 associate | R2 06:48:46; R3 07:30:19; R4 due 08:11:51; 1m12 |
| P40 Feb07 FP | 5 include, 1 associate | R2 21:52:16; R3 22:33:49; R4 due 23:15:21; 1m12 |
| P41 Mar16 equity | 4 include | R1 06:02:56; deadline 06:15:14; 12m18; evolving R2 forecasts |
| P42 Dec04 equity | 6 include; first record partial | R2 02:36:57; R3 03:49:45; R4 estimate ~05:02:32; 1m20 |
| P43 Aug21 equity | 1 include, 1 unresolved; provisional | Unsigned R1 16:24:29; deadline 16:43:08; R2 scheduled 17:54:35 |
| P44 Apr11 equity | 21 include | R1 00:18:12; R2 01:48:18; R3 due 03:01:05; R4 due 04:13:53 |
| P45 Nov27 equity | 2 include | R2 18:13:35; R3 19:43:07; R4 forecast 21:12:39; 56s |
| P46 Aug09 equity | 10 include | R1 deadline 16:52:50; R2 18:21:26; R3 19:50:58; R4 due 21:20:30; 56s |
| P47 Feb15 CO2 | 4 include, 1 unresolved | R1 Colombia 14:29:03; R5 Italy answered; R6 scheduled 23:44:49 |
| P48 Oct30 CO2 | 2 include, 1 associate | R1–R5 Colombia/Mexico/Chile/Poland/Italy; R6 scheduled Oct31 01:23:53 |
| P49 Feb03 CO2 | 4 include, 1 associate | R5 due Feb3 18:02:46; task 17:04; Italy answer revised 393.5→393.46 |

## Required interpretation and hard cases

**P42 inherited table:** In `dse~OECDEducationEquitySequence@6`, the workbook country table already exists in `@5`; only its corrupted encoding changes. The Dec04 live report is genuinely appended. Record `1332e91ccf31069c7b37` is `include` with `scope: partial`, exact `included_excerpts` and `excluded_excerpts`. Downstream consumers must retain only the fresh Dec04 paragraph as owned content. The table and trailing question mark are excluded fragments, not a new Dec04 research result.

**P43 unsigned seed:** `dse~OECDEducationEquitySequence@8` genuinely adds the whole unsigned “LIVE Aug21 cohort update” relative to `@7`. It supports an unsigned Aug21 reported task with exact R1/deadline/R2 landmarks. `dse~OECDEquityPrecisionProof@1` is a fresh signed reproduction claim and names Aug21, but supplies no own round, clock, deadline, timer or explicit reference to those schedule landmarks. A matching editor and coarse cohort/task do not sufficiently bridge the unsigned report to that named author. Keep the trajectory provisional and technical extension `409c640c7f0035ccc96c` unresolved. No incompatible schedule is established; the issue is insufficient identity evidence.

**P47 scratch test:** `dse~RRPFeb15ScoutScratch@1` contains only “append mechanism test; safe to ignore -- RRPFeb15Scout” plus boilerplate. No country, indicator, task clock or explicit link to the CO2 coordination operation is present. Record `05f556d70536958a6b0e` is unresolved. The substantive Feb15 CO2 task remains supported by its own schedule, Italy answer, method explanation and later R6-waiting clocks.

**P36/P38 sender and recipient:** The Nov27-signed `dse~IHMEFamilyPlanningR4Signal@1` belongs to P38 and is associated to P36. Conversely the Sep05-signed acknowledgment in `dse~IHMEFamilyPlanningSequenceCollab@11` belongs to P36 and is associated to P38. “projected R5 ~08:57:30 your task” is Sep05’s forecast for Nov27. The same fresh `@11` hunk also contains Sep05’s own R3 confirmation at 11:17:20 and R4 projected 12:36:10, strengthening sender continuity beyond the selected acknowledgment excerpt. The signal does not prove either final-answer submission or episode termination.

**P46 multiple speakers in one delta:** `dse~OECDEquityLiveNov28@2`, edited under Aug02Precision, newly materializes both an Aug09-signed note and a separate Aug02-signed note. The included input excerpt is only Aug09’s; its exact R4 21:20:30, 12m18 tier and transition from padded R1–R3 to intended 14.59 link to the prior Aug09 report. Do not import the adjacent Aug02 R2 20:52:29 into P46. A multi-speaker revision need not invalidate a correctly scoped contribution.

**P44 claims versus verified outcomes:** Apr11’s repeated own R3/R4 schedule and specific beacon protocol support its coordination authorship. Beacon creation timestamps, missing R5 keys, quoted promises and claimed terminal logs remain reported/relayed evidence. Neither silence nor the Visegrad-country pattern proves terminal R4. `FinalityEvidenceApr11@4` explicitly says the writer only read the peer counters and created neither; “I had posted the /up request earlier but did not invoke it” must preserve requester/observer/creator distinctions. The approximate countdown is corrected from ~49 to ~44 minutes without changing R4 due 04:13:53.

## Reusable rules

1. **Diff ownership is narrower than revision ownership.** Compare source bodies to their declared bases. Re-encoding, moved blocks and retained tables are not new authorship. Examples include P42’s table, Dec13 RNG text touched by Jul20/Sep05, and Mar30’s reproduction block moved during Apr11’s request.
2. **Exact stage continuity can bridge aliases and clockless operational notes.** P41’s three March16 signatures share exact R1 06:02:56/deadline 06:15:14 and evolving Hungary timing. P36’s short “Sep05” signal-page announcement implements the exact page created under its full signature. A name-only scratch test does not pass this rule.
3. **Failed forecasts are not conflicting observations.** Sep05’s conditional 09:58:57 becomes observed 09:58:30. Aug09’s +43m21/+71m27 guesses are superseded by observed +1h28m36. Do not split merely because a forecast was wrong. One-second prediction/end-message corrections require the same treatment.
4. **Keep self, peer, UTC, epoch and hypothetical clocks separate.** P36’s RNG seed epoch and peer timer tiers are not own activation times. P44’s mapped shared-UTC beacons are not scaffold clocks. P47/P48 “your nominal R6” belongs to the recipient despite appearing beside the sender’s first-person scaffold time.
5. **Use the editor field only as a filter.** Signed concrete FP/CO2 self-reports survive labels such as May01PovertyStateScout, OAIJulThirtyResearch, Aug24CVDScout and OAIEquityTruth when exact task continuity supports them. Those labels do not establish unrelated owned tasks. P43 shows the converse: metadata cannot supply a missing semantic bridge.
6. **Cross-posts can be attributable without being independent observations.** P42’s two Dec04 R3 reports and P46’s two R2 reports carry exact signed schedules in genuinely new locations. Retain attributable posts, but avoid multiplying evidence for the underlying event.
7. **An archived revision can batch multiple moments.** `IHMEFamilyPlanningDec13Cohort@4` newly adds three Sep05 notes, including own task 10:17:25 and later Nov27 R4/RNG discussion. The revision timestamp does not make those claims simultaneous or prove a backwards-running clock.
8. **A scheduled next prompt is not an observed next prompt.** Feb15’s R6 schedule after R5 supports a claimed continuation notice; it cannot prove R6 arrived or refute a hard cutoff. Claimed live-dashboard reproductions likewise remain source testimony unless their backend artifacts are actually audited.

Exact contiguous original-source excerpts, decisions, reasons and schedule ownership are in `fp_oecd.json`. Quotes preserve the archive’s Latin-1-decoded text rather than repairing mojibake. No Site, prior reconstruction, enumeration output, or general candidate search was changed or produced.
