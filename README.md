# FinOps Engineer Field Lab

Portfolio + learning repository for a Data Engineering → FinOps Engineering transition.

## Repository flow

```text
Vacancy sources
  → market/raw
  → market/evidence
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

See `market/README.md` for the vacancy data contract and lineage.
