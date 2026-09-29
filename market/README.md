# Malaysia FinOps Engineer Vacancy Census

This folder is the canonical location for vacancy research datasets.

## Data lineage

```text
source URL / job page
  → raw/              original capture or extracted source record
  → evidence/         traceability metadata and source checks
  → canonical CSV/JSON
  → vacancy_skill_matrix.csv
  → frequency datasets
  → ../docs/MARKET_ANALYSIS.md
```

## Population rule

Include only Malaysia vacancies that are active when checked and whose job title contains the contiguous phrase `FinOps Engineer`. If fewer than 50 verified roles exist, stop at the verified population instead of padding with related titles.

## Canonical outputs

- `malaysia_finops_engineer_vacancies.csv`
- `malaysia_finops_engineer_vacancies.json`
- `vacancy_skill_matrix.csv`
- `skill_frequency.csv`
- `finops_capability_frequency.csv`
- `cloud_frequency.csv`
- `platform_frequency.csv`
- `language_frequency.csv`
- `bi_tool_frequency.csv`
- `industry_frequency.csv`
- `seniority_frequency.csv`

## Supporting folders

- `raw/` — one raw record/capture per source before normalization.
- `evidence/` — URL, checked date, active-status evidence and extraction notes.
- `schemas/` — canonical schema/data contract.
- `quality/` — validation results, duplicate checks, exact-title checks and population reconciliation.

## Recommended vacancy ID

`MY-FE-0001`, `MY-FE-0002`, ...

Never reuse an ID for a different vacancy.
