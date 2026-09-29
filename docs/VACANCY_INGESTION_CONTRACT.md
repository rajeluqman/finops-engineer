# Vacancy Ingestion Contract

## Purpose

Create one repeatable path from a live Malaysia FinOps Engineer vacancy to auditable market datasets.

## Lifecycle

```text
DISCOVER
  ↓
ASSIGN IMMUTABLE ID
  ↓
CAPTURE RAW SOURCE FIELDS
  ↓
VERIFY ACTIVE + TITLE + MALAYSIA SCOPE
  ↓
RUN VALIDATION
  ↓
CLASSIFY SKILLS/CAPABILITIES
  ↓
CANONICAL POPULATION
  ↓
AGGREGATE FREQUENCIES
  ↓
MARKET ANALYSIS
```

## Step 1 — Assign ID

Use the next unused ID:

```text
MY-FE-0001
```

ID behaves like a primary key. Never recycle it for another vacancy.

## Step 2 — Raw record

Copy `market/templates/vacancy_record.template.json` to:

```text
market/raw/MY-FE-0001.json
```

Populate source-derived fields. Keep vacancy wording separate from your interpretation.

## Step 3 — Evidence record

Copy `market/templates/evidence_record.template.json` to:

```text
market/evidence/MY-FE-0001.json
```

Record the verification timestamp and evidence for active status, exact title, and Malaysia scope.

## Step 4 — Pre-build validation

```bash
make market-check
```

Fix hard contract failures before building derived outputs.

## Step 5 — Deterministic classification

The builder scans the four source-text fields against `market/schemas/signal_taxonomy.json`.

A keyword match creates a candidate signal. For example:

```text
"Terraform automation on AWS"
        ↓
terraform = true
automation = true
aws = true
```

If the deterministic rule is wrong for a specific vacancy, document the correction using `manual_overrides`:

```json
{
  "manual_overrides": {
    "python": false,
    "terraform": true
  }
}
```

This is preferable to silently editing generated CSV columns.

## Step 6 — Eligibility gate

Canonical inclusion requires all of the following:

```text
raw.active_status = true
AND evidence.active_status = true
AND raw.job_title contains contiguous "FinOps Engineer"
AND evidence.title_verified = true
AND evidence.malaysia_verified = true
AND raw.job_url = evidence.job_url
AND raw.source = evidence.source
AND vacancy_id unique
AND job_url unique
```

Related titles are valid research leads but are not canonical census members.

## Step 7 — Build

```bash
make market-build
```

Generated outputs:

```text
market/malaysia_finops_engineer_vacancies.csv
market/malaysia_finops_engineer_vacancies.json
market/vacancy_skill_matrix.csv
market/skill_frequency.csv
market/finops_capability_frequency.csv
market/cloud_frequency.csv
market/platform_frequency.csv
market/language_frequency.csv
market/bi_tool_frequency.csv
market/industry_frequency.csv
market/seniority_frequency.csv
market/quality/latest_validation.json
docs/MARKET_ANALYSIS.md
```

## Step 8 — Review QA report

Never quote the requested target as though it were observed market size.

Report exactly:

```text
Target population requested: 50
Verified active exact-title population: N
Coverage achieved: N / 50
```

## Source fact vs derived analysis

### Source fact

Raw title, description, requirements, location, source URL, active state evidence.

### Deterministic derived signal

Keyword-classified fields such as `terraform = true` or `rightsizing = true`.

### Human analysis

Why the market signal matters, interview-risk interpretation, learning priority, and resume gap.

Do not collapse these three layers into one.

## Change control

When a vacancy expires later, do not delete its historical ID. Update/recheck the research record according to the study methodology. The canonical active census should always represent the intended collection snapshot, while source history remains traceable in Git.
