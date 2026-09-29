# Market Census Builder

`build_market_census.py` is the deterministic build step for vacancy research.

## WHAT

Reads candidate vacancies and evidence records, validates the contract, classifies configured signals, filters the canonical population and regenerates market datasets.

## WHY

Without a deterministic build, manual spreadsheet edits make it difficult to prove where a count came from or reproduce market-analysis results.

## WHEN

Run after adding, removing, rechecking, or correcting any vacancy record.

## Commands

```bash
python python/market_census/build_market_census.py --validate-only
python python/market_census/build_market_census.py
```

## Output behavior

The full build rewrites only generated market outputs and `docs/MARKET_ANALYSIS.md`. Raw records and evidence are never rewritten.

## Performance note

The target census is at most tens of records, so a simple in-memory standard-library build is intentionally preferred over Spark/Pandas. Complexity is approximately O(records × taxonomy terms), which is negligible at this scale and keeps the repository dependency-free.
