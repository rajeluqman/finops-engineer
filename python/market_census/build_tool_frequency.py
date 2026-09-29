#!/usr/bin/env python3
"""Generate the Checkpoint-1 tool frequency dataset from canonical vacancies."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MARKET = ROOT / "market"
INPUT = MARKET / "malaysia_finops_engineer_vacancies.csv"
OUTPUT = MARKET / "tool_frequency.csv"

TOOLS = [
    "terraform", "bicep", "cicd", "api", "automation", "kubernetes",
    "databricks", "snowflake", "fabric", "power_bi", "tableau", "excel",
]


def as_bool(value: str) -> bool:
    return str(value).strip().casefold() in {"true", "1", "yes"}


def main() -> int:
    with INPUT.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    denominator = len(rows)
    output_rows = []
    for tool in TOOLS:
        count = sum(as_bool(row.get(tool, "")) for row in rows)
        percentage = round(count / denominator * 100, 2) if denominator else 0.0
        output_rows.append({"tool": tool, "count": count, "percentage": percentage})

    output_rows.sort(key=lambda row: (-row["count"], row["tool"]))
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["tool", "count", "percentage"])
        writer.writeheader()
        writer.writerows(output_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
