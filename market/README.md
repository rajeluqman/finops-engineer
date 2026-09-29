# Malaysia FinOps Engineer Vacancy Census

This folder is the canonical location for Malaysia vacancy research datasets.

## Population contract

Target up to **50 currently active Malaysia vacancies** whose job title contains the contiguous phrase `FinOps Engineer`.

Accepted examples:

- `FinOps Engineer`
- `Senior FinOps Engineer`
- `FinOps Engineer II`
- `Lead FinOps Engineer` when the role is still an IC-oriented engineering role

Excluded examples:

- `FinOps Analyst`
- `Cloud Cost Analyst`
- `Cloud Economics Analyst`
- `Cloud Financial Management Analyst`
- `TBM Analyst`
- `Cloud Governance Engineer`
- `Cloud Cost Engineer`

If the verified active market contains fewer than 50 matching vacancies, stop at the verified population `N`. Never pad with related titles.

## Data lineage

```text
source URL / job page
  → raw/              extracted source record; source text preserved
  → evidence/         active/title/location verification
  → quality gates     schema, ID, URL, duplicates, evidence pairing
  → canonical CSV/JSON
  → vacancy_skill_matrix.csv
  → frequency datasets
  → ../docs/MARKET_ANALYSIS.md
```

## One vacancy = one stable ID

Use sequential immutable IDs:

```text
MY-FE-0001
MY-FE-0002
MY-FE-0003
```

Never reuse an ID for a different vacancy, including after a vacancy expires.

## Input pair

For each vacancy create:

```text
raw/MY-FE-0001.json
evidence/MY-FE-0001.json
```

Start from the files under `templates/`.

The raw record stores source-derived vacancy fields. The evidence record separately proves whether it is eligible for the canonical active-Malaysia exact-title population.

## Skill extraction

`schemas/signal_taxonomy.json` defines deterministic keyword rules for cloud, FinOps capability, engineering and stakeholder signals.

`manual_overrides` in the raw record may correct a false positive/negative. Overrides must be explicit booleans and may only target registered taxonomy fields.

Automation does **not** infer active status, Malaysia scope, industry, company type or source credibility.

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

## Quality output

`quality/latest_validation.json` records:

- target population
- raw/evidence counts
- verified canonical count
- rejected count
- rejection reason per vacancy
- coverage `N / 50`

## Commands

```bash
make market-check
make market-build
make test
```

`make market-check` is safe for pre-commit validation because it does not rewrite generated datasets.
