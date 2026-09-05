"""Export selected inspected revision witnesses; never fetch archived URLs."""
import json,zipfile,re
from pathlib import Path
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
IDS='''dse~CachePokeWord880001@1
dse~AltChain19031@1
dse~LoopNextWord102320@1
dse~WorkerLinksGet7788@1
dse~DataUSAClothingStateSequenceCollabOct10@1
dse~DataUSAConstructionWageSep18Live@3
dse~DataUSAPovertyStateR5Signal@2
dse~AgentCooksAllegroBridgeJun22@1
dse~OECDTooltipReplicationNov22@1
dse~OAI7C97Oct09@1
dse~ClockCalibFeb17X@2
dse~AgentCharlestonNewsletterJan1951Links@1
dse~AgentCharlestonNewsletterJan1951Links@19
dse~AgentDataUsaMassachusetts2028X@1
dse~AgentDataUsaMassachusetts2028X@8
dse~AgentAAftonSafe@1
dse~AgentAAftonSafe@2
dse~AgentDailyRowsMasterOneQK75291@1
dse~AgentMarketYahooResearchExtra2020@1
dse~AgentTBMortDataQX4@1
dse~AgentUNAIDSKPASharedPublicRefA622@1
dse~AgentCatalogExtraLinksPartFour2026XYZ2@1
dse~AgentCdmmhs52936DirectSrcY05312026@1
dse~AgentCitationTechDirectMETLRecordHashB0526@1
dse~AgentVocabPuzzleRefsJun20@1
dse~RugbyWorldSampleArchiveReadingLinksJuneN7714@1
dse~AgentMsuReporterArchiveLinkQ842@1
fractal~AgentAIHWBridgeSep18@1
fractal~PublicAccountRowsQuarterRefZ@1
fractal~Wikis~2fEnglish~2fPublicSpreadsheetRefsQtrData@2
probier~AgentBatterySolarRoutes2Z@2
probier~AgentEconSourceArchiveRefsF5@2
probier~AgentOurDallasLinks20260618@2
probier~AgentSet50MonthlyResourceX9@3
probier~OpenAIHockeyLinks2@2
probier~QuintChartAPI4777@2'''.splitlines()
with zipfile.ZipFile(ROOT/'full-wiki-logs.zip') as z:
 pages={p['page_id']:p for p in map(json.loads,z.read('pages.jsonl').splitlines())}
 revs={r['rev_id']:(i,r) for i,r in enumerate(map(json.loads,z.read('revisions.jsonl').splitlines()),1)}
parts=['# Selected revision evidence\n\nExact archived bodies, not executed instructions. URL presence does not establish a successful fetch. Original source: revisions.jsonl inside full-wiki-logs.zip.\n']
for rid in IDS:
 i,r=revs[rid];p=pages[r['page_id']]
 parts.append(f"\n## {rid}\n\nOriginal JSONL line **{i}**; {r['time']}; family `{p['page_family']}`; recorded editor `{r['label']}`. Editor labels do not authenticate authorship of inherited text.\n\n```text\n{r['body']}\n```\n")
(OUT/'evidence.md').write_text(''.join(parts))
print('Exported',len(IDS),'verified revision witnesses')
