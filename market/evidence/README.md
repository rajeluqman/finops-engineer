# Vacancy Evidence Records

Evidence is deliberately separate from extracted vacancy text.

For every `market/raw/MY-FE-XXXX.json`, create a matching:

```text
market/evidence/MY-FE-XXXX.json
```

Use `../templates/evidence_record.template.json`.

## Required checks

- `active_status` — vacancy is active at collection time.
- `title_verified` — observed title contains the contiguous phrase `FinOps Engineer`.
- `malaysia_verified` — source supports Malaysia scope.
- `job_url` — must exactly match the raw record.
- `source` — must exactly match the raw record.
- `checked_at` — ISO-8601 timestamp for the verification event.

Text fields such as `status_evidence`, `title_evidence`, and `location_evidence` should describe what was actually observed. Do not invent evidence when a source does not disclose it.
