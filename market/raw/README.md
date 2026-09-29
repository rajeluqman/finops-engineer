# Raw Vacancy Records

Store exactly one JSON record per candidate vacancy using the stable vacancy ID as the filename.

```text
MY-FE-0001.json
MY-FE-0002.json
```

Use `../templates/vacancy_record.template.json` as the starting contract.

## Rules

1. Preserve the vacancy wording in `role_summary`, `responsibility_text`, `requirement_text`, and `preferred_text`; do not rewrite it as analysis.
2. `date_checked` is the date the source was reviewed.
3. `job_url` must point to the source actually reviewed.
4. Do not manually set derived taxonomy columns in this file. Use `manual_overrides` only when the deterministic classifier needs correction.
5. An input record is not automatically part of the canonical census. Eligibility is decided with the matching record under `../evidence/`.

Optional source captures such as `.md` or `.txt` may be kept beside the JSON using the same vacancy ID. The build only reads `*.json`.
