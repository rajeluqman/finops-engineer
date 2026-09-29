# FinOps Engineer Field Lab

Portfolio + learning repository for a Data Engineering → FinOps Engineering transition.

## Repository flow

```text
Vacancy sources
  → market/raw
  → market/evidence
  → validation gates
  → canonical vacancy dataset
  → skill/capability frequency outputs
  → docs/MARKET_ANALYSIS.md
  → knowledge map + case studies + labs
  → Power BI
  → interview evidence
```

## Core rules

- Malaysia vacancy census targets active roles whose job title contains the contiguous phrase `FinOps Engineer`.
- Do not pad the dataset with related job titles if the verified population is smaller than the target.
- Keep source facts, analysis, and reproduction labs separate.
- Keep potential, projected, and realized savings separate.
- Every optimization lab must validate cost, technical, and business/SLA impact where applicable.

## Market census commands

```bash
make market-check   # validate raw + evidence without writing derived outputs
make market-build   # rebuild canonical datasets, frequencies, QA report and market analysis
make test           # run unit tests
```

Python 3.12+ is recommended. The market census builder uses only the Python standard library.

## Vacancy ingestion contract

Every candidate vacancy uses the same ID in both locations:

```text
market/raw/MY-FE-0001.json
market/evidence/MY-FE-0001.json
```

A record reaches the canonical population only when all gates pass:

```text
valid raw record
+ matching evidence record
+ active vacancy
+ exact contiguous title phrase "FinOps Engineer"
+ Malaysia scope verified
+ matching URL/source
+ unique vacancy ID and URL
= canonical record
```

See `docs/VACANCY_INGESTION_CONTRACT.md` for the full workflow.

## Main areas

- `market/` — vacancy census, raw evidence, canonical datasets, derived matrices and frequencies.
- `docs/` — analysis, knowledge map, KPI dictionary, decision trees, guardrails, interview guide and source register.
- `research/` — framework, provider documentation and published company cases.
- `case_studies/` — deep case-study work.
- `labs/` — reproducible FinOps experiments.
- `data/` — lab/project data lifecycle: raw → bronze → silver → gold.
- `sql/`, `python/`, `terraform/`, `bash/`, `powershell/` — implementation artifacts by language/tool.
- `powerbi/`, `tableau/` — dashboard artifacts.
- `evidence/` — baselines, experiments, validation outputs and screenshots.
- `interview/` — question bank, scenarios and answer cards.
