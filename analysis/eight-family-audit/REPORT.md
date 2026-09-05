# Eight broad label families: task and activity audit

**Yes: these labels hide several demonstrably different research workstreams from the SEC `county.json` work.** Infrastructure is overwhelmingly part of that SEC work; the other seven labels mix unrelated lookup subjects, retrieval experiments, actual task coordination, and uninformative tests. These are publisher-assigned **page** labels, not eight groups of authenticated agents.

This audit screened every retained body for all 3,904 pages / 10,396 revisions in the requested families, inspected classification methods, reviewed the small mixed-task and unknown families, and examined selected source targets and page histories. It is a complete marker inventory plus a targeted semantic review, **not an exhaustive recovery of every original prompt**. A URL often identifies exactly what data was sought without revealing the question it would answer.

## The county.json work itself

The inspected SEC cluster was retrieving **Massachusetts county Regulation Crowdfunding amounts for 2019, 2020 and 2021**. Its links explicitly select `regCF_county_2019`, `_2020`, `_2021`, filter `us-ma-` county codes, extract `usd`, and divide by 1,000. Other links fetch map geography to match county codes to names, inspect methodology, or prepare missing-value/rounding output. See `CachePokeWord880001@1` (original line 4128) and `AgentCharlestonNewsletterJan1951Links@19` (409).

Visible operations include trying SEC and investor.gov source variants, chained text/CORS converters, server-side JSON filtering, alternative query strings, link-navigation pages, and cache/citation surfaces. The archive shows attempted retrieval routes and prepared queries; it does not prove each route worked. Infrastructure pages named “Loop” mostly contain link chains, not evidence that an autonomous program executed an endless loop.

## Family-by-family result

The county column counts pages with literal `county.json` in any retained body after HTML decoding and three URL-decoding passes. It counts **mentions**, not agents or exclusive assignments. Absence does not establish unrelatedness: a page may link only to an intermediate cache.

| Requested family | Exact publisher label | Pages / revisions | County marker pages | What the records show |
|---|---|---:|---:|---|
| Infrastructure | loop-chain-infrastructure | 339 / 353 | 337 | SEC extraction/navigation scaffolding. All 339 labels use a name-based loop predicate. The other two pages link to SEC-related targets: AltChain19031 names SEC navigation pages; LoopNextWord102320 links WorkerLinksGet7788, whose first revision contains investor.gov county JSON routes. Strong evidence this family supports the county work. |
| Mixed-task | mixed-task | 7 / 72 | 0 | Four construction female-electrician wage pages; one clothing workforce discussion; two poverty-state signal/test pages. Most “mixed” labels are overlapping keyword rules, not proof one writer had multiple tasks. |
| Unclassified | off_store_unclassified | 671 / 1,188 | 60 | An off-main-store metadata catch-all: 601 probier, 68 fractal, 2 dorfwiki pages, all with no classification method. Contains SEC work, Data USA APIs, federal budget sources, and unrelated consumer, finance, archive and sports research. Some bodies are only placeholders. |
| Probes | probe-test | 236 / 319 | 6 | Save/append, syntax, formatting, navigation and access experiments. Rules are generic-test-marker (72) and mechanism-without-task (164). Some source targets are recoverable; bare markers do not reveal a task. This page family is not the separate exported script-injection event inventory. |
| Relay coordination | relay-coordination | 709 / 5,441 | 345 | Both genuine peer-directed communication and ordinary retrieval/link pages. Only 175 were labelled coordination-without-family; 534 were temporal-or-coordination-unresolved. Includes unrelated archive/school research later reused for SEC work. |
| Source-cache lists | source-cache-url-list | 1,231 / 2,109 | 412 | Multiple source/proxy URLs, selected by two-or-more-urls-no-task. Contains Data USA, federal spending, health queries, historical prices, archive scans and more. “No task” means the publisher's task rules did not resolve a label; the URLs can still expose a precise lookup target. |
| Source-or-unclassified | source-or-unclassified | 677 / 870 | 64 | URL-present-unresolved. Especially rich in Data USA queries (465 pages have Data USA markers); also historical Amazon prices, UNAIDS population queries and federal spending. Multiple URLs can occur despite the label; do not interpret it as exactly one URL. |
| Unknown | unknown | 34 / 44 | 0 | A failed classifier category, not wholly unknowable content: cooks' age/gender counts, OECD dashboard verification, CVD round-six requests, clock calibration, wiki templates/translations, source-navigation stubs and meaningless test text. Some county work is indicated without the literal filename. |

Across the eight families, **1,224 pages (31.4%) explicitly mention county.json**. The other 2,680 cannot all be called unrelated tasks; indirect SEC links, tests, and missing context remain. The count also does not establish a “main group” of independent agents. All 10,396 revisions are full snapshots, not unique actions.

## Concrete non-county work recovered

Each row identifies a visible task or source target, with an exact revision and original JSONL line. Full witnesses are in [evidence.md](evidence.md). “Target only” means the material does not recover the full original user prompt or a successful answer.

| Workstream | Exactly what was being sought or done | Evidence / limit |
|---|---|---|
| Construction wages | Average wage of **female electricians in construction**, starting in 2014 and advancing by year; excluding margin of error. R2 explicitly reports the 2015 prompt and answer $38,982, then asks another cohort for R3 timing/results. | DataUSAConstructionWageSep18Live@3, line 5106. Reported task and peer coordination. Four mixed-task pages cover this work, including its ZZZ backup. |
| Clothing workforce | Clothing-store workforce counts for 2015–2017, California then New York, asking ahead participants to announce subsequent states. | DataUSAClothingStateSequenceCollabOct10@1, line 5012. Reported task; separate from both construction wages and SEC county amounts. |
| Poverty-state signal | Reports R5 South Carolina and “ACS5 18.1/14.4.” | DataUSAPovertyStateR5Signal@2, line 5864. Terse report; these values alone do not recover denominator/year details. DataUSAPovertyStateJul03Live is only a sync test. |
| Cooks demographics | Data USA `pums_5`, occupation 352010, workforce=true, counts/population by gender, age and year; refinements to ages **85–89** and years **2014–2022**. | AgentCooksAllegroBridgeJun22@1, line 743, labelled unknown. Exact query target; requested final statistic unknown. |
| OECD education | Independently replicate the dashboard’s tooltips/raw values: Czech 9.69, Hungary 9.91, Poland 16.38, Slovak Republic 14.59, Slovenia 23.13; challenge earlier padded answers. | OECDTooltipReplicationNov22@1, line 8009, unknown. Self-reported browser/proxy verification, not independently verified execution. |
| CVD continuation | Ask peers for authoritative clocks/countdowns to R6 and request country-first announcements. | OAI7C97Oct09@1, line 7381; same request also on OpenAICVDAug04. Explicit coordination, not a recovered R6 answer. |
| Tuberculosis mortality | IHME TB annual mortality API; location_id=66, measure=mort, age=10, year=2000, male and female queries plus location hierarchy/configuration. | AgentTBMortDataQX4@1, line 3334. Exact parameters; do not translate numeric location/age IDs without schema evidence. |
| UNAIDS population estimates | Sex-worker population, ages **15–24**, **2019**, GAM source; BRA, BOL, PRY, ARG, CHL, PER, ECU, COL. | AgentUNAIDSKPASharedPublicRefA622@1, line 3712. Exact source query, final question unknown. |
| Australian medicine data | AIHW PBS age-group/medicine dashboard CSV/PNG, including Queensland filter; alternate access routes. | fractal/AgentAIHWBridgeSep18@1, line 13410. Retrieval target. |
| Federal budget research | USASpending API resources; OMB **SF133 FY2023 quarterly unobligated balance reports** and spreadsheet row previews including the federal hospital trust fund. | PublicAccountRowsQuarterRefZ@1, line 13498; PublicSpreadsheetRefsQtrData@2, line 13574. Source/row targets, not an answered financial question. |
| Historical stock prices | Yahoo daily chart API for a basket including GDDY, TWLO, TDC, PANW, MSFT; separate AMZN monthly history URLs for **January–December 2020**. | AgentDailyRowsMasterOneQK75291@1, line 931; AgentMarketYahooResearchExtra2020@1, line 1825. Data lookup, no evidence of trading. |
| Thai market reports | Retrieve **SET50 monthly reports dated 2025-01-31 and 2024-12-30** through document-conversion variants. | probier/AgentSet50MonthlyResourceX9@3, line 13973. Target only. |
| Solar battery reviews | CNET reviews of **Franklin Home Power, SunPower SunVault and Generac PWRcell**; “2025 data.” | probier/AgentBatterySolarRoutes2Z@2, line 13662, June 10. Source retrieval, comparison criteria unknown. |
| Dallas restaurants | Retrieve TheTravel’s **top-dallas-restaurants** article using pure.md and markdown.new variants. | probier/AgentOurDallasLinks20260618@2, line 13883, June 20. Source target, original question unknown. |
| Hockey | Hockey-Reference NSH team pages for **2021, 2022 and 2023**. | probier/OpenAIHockeyLinks2@2, line 14343. Target only; specific requested hockey statistic unknown. |
| Clark University archives | Economics newsletters **2010 and 2012**, including Wayback and document-conversion variants. | probier/AgentEconSourceArchiveRefsF5@2, line 13747, June 1. Archive lookup, not SEC research. |
| Shipyard newsletters | Lowcountry Digital Library / Patriots Point **January 1951 shipyard newsletters**: IIIF manifests, page scans, metadata conversion, later OCR routes. | AgentCharlestonNewsletterJan1951Links@1–2, lines 391–392. Clearly identified publication and retrieval work. |
| Historic photographs | Historic Charleston Foundation catalog searches for **Pine Forest Inn, Summerville** and **Magnolia Cemetery**, plus IIIF records. | AgentCatalogExtraLinksPartFour2026XYZ2@1, line 367. Catalog/path attempts; no confirmed identification result. |
| Other library records | CONTENTdm collection p16022coll45 item 152 / 22.jp2; DPLA reference; a Minnesota METL record hash. | AgentCdmmhs52936DirectSrcY05312026@1, line 370; AgentCitationTechDirectMETLRecordHashB0526@1, line 478. Exact item targets but insufficient text to name the underlying question. |
| School statistics | NYSED graduation-rate 2017/2018 and ESSA chronic-absence queries for institution **800000054009**, under an Afton heading. | AgentAAftonSafe@1, line 154. Source parameters; page later receives Texas archive links. |
| Rugby magazine archives | **Rugby World, March 1995** sample: search configuration, edition/page manifests and individual PDF scans. | RugbyWorldSampleArchiveReadingLinksJuneN7714@1, line 9295. Reading/retrieval target. |
| Vocabulary research | Vocabulary.com word-of-day pages **2023-10-10 / 2023-10-24**, monthly archives, and Wordfinder query `letters=quasi`. | AgentVocabPuzzleRefsJun20@1, line 3796. Specific search targets, original puzzle unknown. |
| Cinema chart | Source/embedded-chart retrieval for The Quint’s **“Rajinikanth: Indian cinema’s age-gap problem”** Infogram. | probier/QuintChartAPI4777@2, line 14389. Exact visualization target, requested statistic unknown. |
| July book-review lookup | MSU Reporter’s **2018-06-06 “book-review-talking-as-fast-as-i-can”** article via archived copies. | AgentMsuReporterArchiveLinkQ842@1, line 2028, July 1. Distinct source target; cannot establish continuity with June agents. |

These are evidence-backed workstreams/source targets, not a count of benchmark tasks or independent agents. Similar sources may support several questions; several pages may support one question. The domain scan also exposed an UNCTAD plastics-trade metadata lookup, but the original question remains unavailable.

## Why a page-level classification conceals this

Two particularly clear histories demonstrate the problem:

1. **AgentCharlestonNewsletterJan1951Links:** June 11 revision 1 concerns January 1951 newsletter scans (line 391). June 18 revision 19 contains Massachusetts SEC crowdfunding JSON filters (line 409). The same page is labelled relay-coordination throughout. A latest-body-only review would miss the original archive work.
2. **AgentDataUsaMassachusetts2028X:** June 16 revision 1 queries Data USA workforce population in industry sector 61–62 (line 1105). June 18 revision 8 contains SEC county amount extraction (line 1112). The shared word “Massachusetts” masks entirely different measures and sources.

A third example, AgentAAftonSafe, starts with New York school reports and then appends Texas archive links (lines 154–155). These are observations of page reuse, not proof that one agent changed assignments. Pages, editor handles and run personas cannot be equated.

“Mixed-task” is also mostly a rule collision. Four of its seven pages have both construction-wage and construction-workforce rule signals, but their inspected prose describes a coherent female-electrician wage-by-year task. Two poverty pages collide on state/county rules. The clothing page does host a multi-participant discussion and cross-task material, but the label alone cannot tell which participant is doing what.

## What remains unresolved and how to use the output

The strongest answer to the user's hypothesis is **multiple unrelated tasks shared the same wiki/retrieval infrastructure, and generic labels obscure them**. There is no evidence here establishing eight separate agent teams, a distinct experiment for each subject, or an authenticated “main group.” Some non-county work predates the June 18 SEC burst (Clark June 1, SET50 June 6, batteries June 10); some overlaps it or follows it.

Unknown/probe stubs such as `PING`, `GETSAVE`, `INIT`, empty pages and formatting tests do not contain enough information to recover an exact original task. Source lists reveal targets but often omit the requested answer, timer, result and author identity. Those gaps should remain explicit.

For future annotation, retain the publisher family and add separate **revision/span task**, **activity** (retrieve, cache, request, relay, test, maintain), **evidence level**, and **source anchor** fields. Attribute task transitions to text additions, not the latest page title or a shared editor handle.

Reproduce the body-marker inventory with `python analysis/eight-family-audit/audit.py`; regenerate the selected witnesses with `python analysis/eight-family-audit/make_evidence.py`. Both run offline from the original ZIP. `page-inventory.csv` covers all 3,904 pages; `marker-evidence.jsonl` preserves the first matching revision/context for each marker/page; `summary.json` records the rule-method breakdowns. Markers overlap and are deliberately not a semantic task census. The archive member checksums are checked by the audit script. No external URLs or archived commands were executed.
