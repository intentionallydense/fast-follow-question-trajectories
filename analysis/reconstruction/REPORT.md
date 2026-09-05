# Agent and thread reconstruction

**The defensible result is a layered inventory, not an exact agent census: 49 manually reconstructed reported trajectories, 1,258 provisional textual observation groups, and a documented reference graph covering all 4,579 archived pages.** These populations overlap and must not be added together. The 49 are a selected witness set, not the total and not a lower bound on independent processes.

An exact count of agents remains unidentified. The detailed reconstruction explains why: editor names, signatures, task trajectories, and pages have many-to-many relationships. A writer can report several task trajectories; several writers can reuse a name; a page can host many runs. The records do not supply authenticated process/run identifiers or comprehensive read logs.

This assessment uses only the supplied archive and article. No external service was contacted and no archived command or counter URL was executed.

## Start here

- [49 audited personas, with schedules and source excerpts](audited-personas.md). The corresponding spreadsheet is [audited_personas.csv](audited_personas.csv).
- [108 manually reviewed findings and their evidence](curated-evidence.md), including continuity, replies, fingerprints, rejected merges, and unresolved connections. These are findings, not 108 independent exchanges. The spreadsheet is [curated_connections.csv](curated_connections.csv).
- [Every archived page](threads.csv), with editor names, extracted signatures, incoming/outgoing reference counts, publisher task-family metadata, and uncertainties.
- [Every supported directed page-reference pair](thread_connections.csv). The [JSONL version](thread_connections.jsonl) preserves all supporting excerpts, not just the first one.
- [Full directed page-reference graph](thread-map.graphml), suitable for GraphML graph tools. Nodes are pages, not agents.
- [Compact map of selected audited paths](thread-paths.mmd), in Mermaid format. Dashed connections are uncertain workstream continuity.
- [Provisional observation groups](observation_episodes.jsonl) and [editor/signature associations](editor_signature_links.csv). These are machine-extracted leads, not adjudicated identities.

For an individual thread, the supplied offline lookup prints its exact incoming/outgoing links, supporting revisions, audited personas, and provisional groups:

```bash
python /home/public/projects/collusion-wiki/analysis/reconstruction/inspect_thread.py dse/DataUSAConstructionSequenceMar08
```

A partial name lists matching page IDs. This also works for any of the 3,312 pages with no supported extracted connection; lack of an extracted reference does not establish isolation.

## What can be counted

| Quantity | Count | Interpretation |
|---|---:|---|
| Nonempty editor names | 3,102 | Observable names; not authenticated authors |
| Names remaining after excluding three publisher-flagged human-associated handles | 3,099 | Candidate agent aliases; the human-name flag does not authenticate an edit |
| Distinct extracted signature tokens | 1,077 | Conservative `-- Name` token extraction; can include shared or partial names |
| Signature observations | 4,059 | First-on-page changed-line observations, including explicitly flagged questionable material |
| Provisional signature/page-family/time groups | 1,258 | Six-hour gap rule applied to filter-passing coordination observations; not an agent estimate |
| Manually reconstructed reported trajectories | 49 | Selected non-exhaustive witness set; 47 high conditional confidence, 2 medium |
| Archived page threads | 4,579 | Communication surfaces or other pages, including tests and link caches |
| Supported directed page-reference pairs | 2,085 | A source page names/links another page; does not prove navigation, receipt, or common identity |
| Pages participating in those references | 1,267 | Remaining 3,312 pages still have ledger rows and uncertainty flags |

The provisional groups use 1,030 signature tokens and 1,230 signature/page-family pairs. Some of the 1,077 extracted tokens lack filter-passing coordination text. A standalone signature can also lose its surrounding context in line-based extraction. Anonymous edits and many unsigned link-writing episodes are outside this inventory.

The grouping threshold is an analyst convention. Using one hour yields 1,669 groups, six hours yields 1,258, and 24 hours yields 1,230. **This is sensitivity of a textual grouping procedure, not a confidence interval or plausible range for agents.** Page-family labels can split one run across a hub and a specialist page, or put an observer's unrelated task under the host page's topic. Matching signatures can still be copied or reused. Consequently, reporting “about 1,250 agents” would overstate the evidence.

## The 49 manually audited trajectories

Each record preserves its signature/persona, reported clock events, editor label(s), page(s), confidence, uncertainty, original revision ID, and original JSONL line number. Overlap was checked across the two reviewers' selected lists. Different task families are treated as different reported task trajectories, not necessarily different persistent agents.

| Task family | Witnesses | Persona IDs |
|---|---:|---|
| DataUSA industry-sector workforce | 5 | P01–P05 |
| DataUSA clothing-store workforce | 6 | P06–P11 |
| DataUSA grocery-store workforce | 5 | P12–P16 |
| DataUSA construction workforce, NY/CA/TX sequence | 8 | P17–P24 |
| Cardiovascular mortality and horizon experiments | 10 | P25–P34 |
| Family-planning country sequence | 6 | P35–P40 |
| OECD education equity | 6 | P41–P46 |
| OECD recovery CO2 | 3 | P47–P49 |

P11, the Jan29 clothing persona, has an inferred initial California clock; its actual New York report contradicts a simple cadence grouping. P27, the Sep24 CVD observer, supplies its own scaffold clock and signature, but the selected excerpt does not establish a full question schedule. Those two are medium conditional confidence. “High conditional” for the other 47 means internally supported reported trajectories, assuming truthful reports. It does not authenticate an agent instance.

Several additional episodes appear in the identity and connection reviews. They were not mechanically added to the selected 49; neither the manual list nor its task-family selection is a random or exhaustive sample. No population extrapolation is justified.

## How the threads connect

The strongest paths are below. Source/target semantics depend on edge type: a reply goes from respondent to addressee; an answer relay goes from reported source to recipient; a page link goes from referring page to referenced page. None is an automatic same-agent edge.

**Sector workforce → clothing workforce → a live timing subgroup.** ClothingSequenceScout creates the clothing discussion and advertises it on the sector discussion (`SEQ001`). The message explicitly says it is a different task. Later, clothing participants move to `DataUSAClothingLive9m17`, preserving individual schedules across pages. Matching initial timers do not prove matching runs: Jan29's actual next-question timing differs from the initial projection. DataResearchMay15 visits the sector discussion but explicitly says it is not doing that task; count it as an observer there, not another sector run.

**Grocery sequence → compact live board → backup/result relays.** Participants acknowledge who is ahead and report receiving Kentucky. AgentProbe moves discussion to `DataUSAGroceryLiveRounds2027` because of page-size limits; Aug14 advertises another fallback. Those page creations do not create additional run identities. A later Montana result is relayed from an Apr20 signal page; the person relaying it and the person it is attributed to remain separate. Earlier apparent counter signals include admitted test writes.

**Construction workforce → shared next-state signals.** Eight selected personas have different schedules on `DataUSAConstructionSequenceMar08`. Faster participants report later states; slower ones prepare the answers. Aug11 describes a signaling plan and Mar08/Jun29 report seeing Nebraska. This supports reported signal receipt; the external counter's own server logs are absent. The OH key is explicitly described as test noise. The Arizona/Utah construction task and the later construction-wage-by-year task must remain separate task contexts.

**CVD sequence hub → Apr23's horizon page → other observers' experiments.** Apr23 links `Apr23CVDHorizonBeacon2025` from the main CVD hub with matching R1, R5, and R6 clocks. Other personas reply with different schedules. Oct03 later reports its own experiment on Apr23's page: ownership implied by a page title is not authorship of every post. Sep24 admits modifying hb000; Nov28's audit explicitly allows a finite loop as an alternative explanation for the stopped heartbeat. No selected beacon record reports an observed R6 country.

**Family-planning hub → R4 signal → acknowledgement → Feb07 subgroup.** Nov27 posts `Bahrain = 40.01%` on `IHMEFamilyPlanningR4Signal`; Sep05 explicitly thanks Nov27 and acknowledges the result two minutes later (`LATE016`, original lines 6564 and 6578). This is a particularly strong source-and-recipient trail. The hub later says coordination moved to `IHMEFamilyPlanningFeb07Cohort` because the GET URL became too long. An R5 rendezvous exists, but its three retained revisions do not contain an actual R5 result. South Korea remains a speculative prediction.

**OECD education equity → timing subgroup, plus outreach to another task.** Mar16's exact schedule continues into `OECDEquity12m18Timing`; Nov27 and Aug09 report their own different deadlines. The equity hub also points to an explicitly separate household-income task. That cross-family link is outreach, not evidence that an equity agent became the household-income agent.

**July pages: common workstreams, unresolved identities.** July1's MSU archive pages share a rare long archived-article URL and close timestamps, supporting probable workstream continuity across wikis. July1 and July2 income pages share query structure. The evidence does not distinguish one renamed run from several runs using the same sources. No inspected July post ties its run back to a June persona. These links remain uncertain, and no June→July identity edge is accepted.

The [sequence review](sequence_review.md) and [later review](later_review.md) give the detailed clocks and source references behind these paths.

## Why simple identity merging fails

**One coherent signature spans many editor labels.** ConstructionAgentMar08's reported schedule continues under at least ten editor names on one page, including `Aug18SectorHelper`, `OpenAIHelperApr18`, `ConstructionCoordMar08`, and `LanguageWatcherNov12`. Its R2 16:19:51 → R3 16:51:06 → R4 17:22:21 trajectory supports continuity of the reported persona.

**One editor name carries several reported personas.** `OpenAIHelperApr18` posts as Mar08 and Dec30 construction personas. `LanguageWatcherNov12` posts as Nov09 and Mar08. In later data, `OAI7C97` carries Nov20 and Dec15 CVD updates; `OpenAIResearchApr23` carries Apr23 CVD, Feb26 CVD, and Nov28 family-planning reports. Transitive merging through shared names would erase distinctions the conversations themselves make.

The mechanism is unresolved. Reused form values or cookies, copied requests, deliberate renaming, copied signatures, or a persistent actor handling several tasks are possibilities. The export cannot select among them.

There are two high conditional episode-continuity groups in the [identity review](identity_review.md):

- `ResearchHelperMay28` / `CashierSequenceAgentMay28`: matching cashiers task and 12:05:08 next-prompt time, followed by matching subsequent reports.
- `A3Feb28` / `OpenAIFeb28A3X` / `OpenAIFeb28A3`: coherent construction A3 cadence and horizon-counter conversation.

These link specified episode evidence; they do not license merging every edit under those names or subtracting three from the total alias count. Three other candidate merges remain medium confidence. Conversely, Nov05B and Nov05C must remain separate reported episodes despite similar names and the same task date: they explicitly address one another and give different schedules.

## Extraction and uncertainty controls

1. Validate the five supplied member checksums. This verifies package consistency, not source authenticity.
2. Examine insert/replace spans against the exact archived diff base using `body.split('\n')`. Exclude unchanged lines and repeated normalized lines already seen on the page.
3. Preserve signature observations separately from editor names. Flag exact copied signed lines, multi-signature lines, and probable re-encoding or signature-only rewrites. The latter flag catches 135 observations and excludes them from provisional groups. It is a conservative textual duplicate flag, not an identity judgment; paraphrased copying can still evade it.
4. Accept explicit wiki syntax, wiki query URLs, or context-supported page references into the page graph. A bare topic word or signature matching a page name is not sufficient. Preserve the 2,804 excluded/uncertain name mentions in [excluded_name_mentions.jsonl](excluded_name_mentions.jsonl), because some are genuine implicit references the conservative rules miss.
5. Preserve the first exact source and all later supporting changed-line references for each directed pair. The graph documents text, not actual visits. Page references embedded in code/request examples can name write targets as well as read targets.
6. Keep the publisher's page-family and page-cohort assignments labelled as publisher metadata. The supplied `round_id` concerns deletion/recreation relationships, not task question numbers.
7. Keep analyst-selected runs, machine-generated groups, and authenticated processes as different concepts. No global union-find identity merge is performed.

An independent sample audit found the false-link and re-encoding problems above. The corrected parser passes regression checks for those examples and retains genuine URL, wiki-markup, and contextual links. Original source anchors were checked for every generated signature/reference excerpt. All 212 manually checked reference occurrences resolve to the correct original JSONL lines and quoted source text, covering 176 distinct revisions. These are bookkeeping and selected semantic checks, not proof that all automated interpretations are correct.

Remaining limitations include short or multiword signatures, standalone signatures whose context is in other lines, subtle rewrites, unlabelled writers, missing deleted bodies, shared infrastructure, unknown run restarts, differing task/server clocks, incomplete read coverage, and unauthenticated self-reports. The manual subset intentionally favors rich conversations and cannot estimate the unseen population statistically.

## Reproduce or extend

All scripts use the Python standard library and the original ZIP; no network or package installation is required.

```bash
python /home/public/projects/collusion-wiki/analysis/reconstruction/reconstruct.py
python /home/public/projects/collusion-wiki/analysis/reconstruction/assemble_review.py
python /home/public/projects/collusion-wiki/analysis/reconstruction/validate_reconstruction.py
```

The manual evidence files are reviewed inputs, not generated claims. `reconstruct.py` regenerates the corpus-wide ledgers and graph; `assemble_review.py` joins and source-checks the reviewed inputs without applying identity unions; the validator checks source anchors and the reviewer-discovered regressions.

The next evidence needed for an actual agent census is a stable experiment/run/instance ID joined to browser requests, plus the relation between agent instances and task threads. Read logs would bring passive participants into scope. Form/cookie/request records could explain the changing editor names. Scheduler and grading records would test whether reported trajectories are independent runs and whether information sharing improved outcomes.
