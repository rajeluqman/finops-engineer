#!/usr/bin/env python3
"""Build and validate the Malaysia FinOps Engineer vacancy census.

WHAT: converts audited raw vacancy records into canonical and derived datasets.
WHY: keeps vacancy research deterministic, traceable, and reproducible.
WHEN: run after adding or changing any market/raw or market/evidence JSON record.

No third-party Python packages are required.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[2]
MARKET = REPO_ROOT / "market"
RAW_DIR = MARKET / "raw"
EVIDENCE_DIR = MARKET / "evidence"
QUALITY_DIR = MARKET / "quality"
TAXONOMY_PATH = MARKET / "schemas" / "signal_taxonomy.json"

TARGET_POPULATION = 50
ID_RE = re.compile(r"^MY-FE-\d{4}$")
TITLE_RE = re.compile(r"\bFinOps Engineer\b", re.IGNORECASE)

BASE_FIELDS = [
    "vacancy_id", "company", "job_title", "seniority", "location",
    "employment_type", "job_url", "source", "date_checked", "active_status",
    "industry", "company_type", "role_summary", "responsibility_text",
    "requirement_text", "preferred_text",
]
TEXT_FIELDS = ["role_summary", "responsibility_text", "requirement_text", "preferred_text"]

DERIVED_OUTPUTS = {
    "cloud_frequency.csv": ("cloud", ["aws", "azure", "gcp", "multi_cloud"]),
    "finops_capability_frequency.csv": ("capability", None),
    "skill_frequency.csv": ("skill", None),
    "platform_frequency.csv": ("platform", ["kubernetes", "databricks", "snowflake", "fabric"]),
    "language_frequency.csv": ("language", ["sql", "python", "bash", "powershell"]),
    "bi_tool_frequency.csv": ("bi_tool", ["power_bi", "tableau", "excel"]),
}


class CensusError(Exception):
    """Raised when the census violates its data contract."""


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CensusError(f"Invalid JSON: {path}: {exc}") from exc


def iter_json_records(directory: Path) -> list[tuple[Path, dict[str, Any]]]:
    records: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(directory.glob("*.json")):
        if path.name.startswith("_"):
            continue
        payload = load_json(path)
        if not isinstance(payload, dict):
            raise CensusError(f"Record must be a JSON object: {path}")
        records.append((path, payload))
    return records


def valid_url(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def valid_date(value: Any) -> bool:
    try:
        date.fromisoformat(str(value))
        return True
    except ValueError:
        return False


def valid_datetime(value: Any) -> bool:
    try:
        datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def validate_raw(record: dict[str, Any], path: Path, signal_fields: set[str]) -> list[str]:
    errors: list[str] = []
    required = ["vacancy_id", "company", "job_title", "location", "job_url", "source", "date_checked", "active_status"]
    for field in required:
        if field not in record or record[field] in (None, ""):
            errors.append(f"{path}: missing required field '{field}'")

    vacancy_id = record.get("vacancy_id")
    if vacancy_id and not ID_RE.fullmatch(str(vacancy_id)):
        errors.append(f"{path}: invalid vacancy_id '{vacancy_id}'")
    if record.get("job_url") and not valid_url(record["job_url"]):
        errors.append(f"{path}: invalid job_url")
    if record.get("date_checked") and not valid_date(record["date_checked"]):
        errors.append(f"{path}: date_checked must be YYYY-MM-DD")
    if "active_status" in record and not isinstance(record["active_status"], bool):
        errors.append(f"{path}: active_status must be boolean")

    overrides = record.get("manual_overrides", {})
    if not isinstance(overrides, dict):
        errors.append(f"{path}: manual_overrides must be an object")
    else:
        for field, value in overrides.items():
            if field not in signal_fields:
                errors.append(f"{path}: unknown manual_overrides field '{field}'")
            if not isinstance(value, bool):
                errors.append(f"{path}: manual_overrides.{field} must be boolean")
    return errors


def validate_evidence(record: dict[str, Any], path: Path) -> list[str]:
    errors: list[str] = []
    required = ["vacancy_id", "checked_at", "active_status", "title_verified", "malaysia_verified", "job_url", "source"]
    for field in required:
        if field not in record or record[field] in (None, ""):
            errors.append(f"{path}: missing required field '{field}'")
    if record.get("vacancy_id") and not ID_RE.fullmatch(str(record["vacancy_id"])):
        errors.append(f"{path}: invalid vacancy_id")
    if record.get("checked_at") and not valid_datetime(record["checked_at"]):
        errors.append(f"{path}: checked_at must be ISO-8601 datetime")
    if record.get("job_url") and not valid_url(record["job_url"]):
        errors.append(f"{path}: invalid job_url")
    for field in ["active_status", "title_verified", "malaysia_verified"]:
        if field in record and not isinstance(record[field], bool):
            errors.append(f"{path}: {field} must be boolean")
    return errors


def keyword_match(text: str, keyword: str) -> bool:
    text_l = text.casefold()
    keyword_l = keyword.casefold()
    if re.fullmatch(r"[a-z0-9+#.]+", keyword_l):
        return bool(re.search(rf"(?<![a-z0-9]){re.escape(keyword_l)}(?![a-z0-9])", text_l))
    return keyword_l in text_l


def flatten_taxonomy(taxonomy: dict[str, Any]) -> tuple[list[str], dict[str, list[str]], dict[str, list[str]]]:
    fields: list[str] = []
    keywords: dict[str, list[str]] = {}
    groups: dict[str, list[str]] = {}
    for group, mapping in taxonomy.items():
        groups[group] = []
        for field, terms in mapping.items():
            if field in keywords:
                raise CensusError(f"Duplicate taxonomy field: {field}")
            fields.append(field)
            groups[group].append(field)
            keywords[field] = terms
    fields.append("multi_cloud")
    groups.setdefault("cloud", []).append("multi_cloud")
    return fields, keywords, groups


def classify(record: dict[str, Any], signal_fields: list[str], keywords: dict[str, list[str]]) -> dict[str, bool]:
    text = "\n".join(str(record.get(field) or "") for field in TEXT_FIELDS)
    signals: dict[str, bool] = {}
    for field in signal_fields:
        if field == "multi_cloud":
            continue
        signals[field] = any(keyword_match(text, term) for term in keywords.get(field, []))

    signals["multi_cloud"] = sum(bool(signals.get(cloud)) for cloud in ["aws", "azure", "gcp"]) >= 2
    for field, value in record.get("manual_overrides", {}).items():
        signals[field] = value
    if not any(signals.get(cloud) for cloud in ["aws", "azure", "gcp"]):
        signals["multi_cloud"] = bool(record.get("manual_overrides", {}).get("multi_cloud", False))
    return signals


def canonicalize(raw: dict[str, Any], evidence: dict[str, Any], signal_fields: list[str], keywords: dict[str, list[str]]) -> dict[str, Any]:
    result = {field: raw.get(field) for field in BASE_FIELDS}
    result["active_status"] = bool(evidence["active_status"])
    result.update(classify(raw, signal_fields, keywords))
    return result


def eligibility_reasons(raw: dict[str, Any], evidence: dict[str, Any] | None) -> list[str]:
    reasons: list[str] = []
    if evidence is None:
        return ["missing_evidence"]
    if not raw.get("active_status") or not evidence.get("active_status"):
        reasons.append("inactive")
    if not TITLE_RE.search(str(raw.get("job_title", ""))):
        reasons.append("title_not_exact_phrase")
    if not evidence.get("title_verified"):
        reasons.append("title_not_verified")
    if not evidence.get("malaysia_verified"):
        reasons.append("malaysia_not_verified")
    if raw.get("job_url") != evidence.get("job_url"):
        reasons.append("url_mismatch")
    if raw.get("source") != evidence.get("source"):
        reasons.append("source_mismatch")
    return reasons


def ensure_unique(records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    ids = Counter(str(r.get("vacancy_id")) for r in records)
    urls = Counter(str(r.get("job_url")) for r in records)
    errors.extend(f"duplicate vacancy_id: {key}" for key, count in ids.items() if key and count > 1)
    errors.extend(f"duplicate job_url: {key}" for key, count in urls.items() if key and count > 1)
    return errors


def write_csv(path: Path, rows: Iterable[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json.dumps(value) if isinstance(value, (list, dict)) else value for key, value in row.items()})


def frequency_rows(records: list[dict[str, Any]], names: list[str], label: str) -> list[dict[str, Any]]:
    denominator = len(records)
    rows = []
    for name in names:
        count = sum(bool(record.get(name)) for record in records)
        rows.append({label: name, "count": count, "percentage": round((count / denominator * 100) if denominator else 0.0, 2)})
    return sorted(rows, key=lambda row: (-row["count"], row[label]))


def categorical_frequency(records: list[dict[str, Any]], field: str, label: str) -> list[dict[str, Any]]:
    denominator = len(records)
    counter = Counter(str(r.get(field)).strip() for r in records if r.get(field) not in (None, ""))
    return [
        {label: value, "count": count, "percentage": round(count / denominator * 100, 2) if denominator else 0.0}
        for value, count in sorted(counter.items(), key=lambda item: (-item[1], item[0].casefold()))
    ]


def markdown_table(rows: list[dict[str, Any]], label: str, limit: int = 15) -> str:
    if not rows:
        return "_No verified records yet._"
    lines = [f"| {label} | Count | % |", "|---|---:|---:|"]
    for row in rows[:limit]:
        lines.append(f"| {row[label]} | {row['count']} | {row['percentage']:.2f} |")
    return "\n".join(lines)


def render_market_analysis(records: list[dict[str, Any]], groups: dict[str, list[str]], rejected: list[dict[str, Any]]) -> str:
    cloud = frequency_rows(records, ["aws", "azure", "gcp", "multi_cloud"], "cloud")
    finops = frequency_rows(records, groups["finops_capability"], "capability")
    engineering = frequency_rows(records, groups["engineering"], "skill")
    industry = categorical_frequency(records, "industry", "industry")
    seniority = categorical_frequency(records, "seniority", "seniority")
    stakeholders = frequency_rows(records, groups["stakeholder"], "stakeholder")
    n = len(records)
    return f"""# Malaysia FinOps Engineer Market Analysis\n\n> Auto-generated by `python/market_census/build_market_census.py`. Do not hand-edit generated tables.\n\n## Population\n\n- Target population requested: **{TARGET_POPULATION}**\n- Verified active exact-title population: **{n}**\n- Coverage achieved: **{n} / {TARGET_POPULATION}**\n- Rejected/non-canonical raw records: **{len(rejected)}**\n\nThe canonical population contains only records with matching evidence confirming active status, Malaysia scope, and the contiguous title phrase `FinOps Engineer`.\n\n## Most demanded FinOps responsibilities\n\n{markdown_table(finops, 'capability')}\n\n## Cloud platforms\n\n{markdown_table(cloud, 'cloud')}\n\n## Engineering / automation skills\n\n{markdown_table(engineering, 'skill')}\n\n## Industries\n\n{markdown_table(industry, 'industry')}\n\n## Seniority\n\n{markdown_table(seniority, 'seniority')}\n\n## Stakeholder expectations\n\n{markdown_table(stakeholders, 'stakeholder')}\n\n## Certification demand\n\n_Not automatically inferred by this pipeline yet. Certification claims require explicit source-backed extraction during market review._\n\n## Recurring interview-risk areas\n\n_Derive after the verified census is populated. Do not infer market risk from an empty or partial population._\n\n## Resume-to-market gaps\n\n_Derive after the verified census is populated and compare against a versioned resume/profile input. This report does not silently use personal profile data._\n"""


def build(write_outputs: bool = True) -> dict[str, Any]:
    taxonomy = load_json(TAXONOMY_PATH)
    signal_fields, keywords, groups = flatten_taxonomy(taxonomy)
    signal_set = set(signal_fields)

    raw_pairs = iter_json_records(RAW_DIR)
    evidence_pairs = iter_json_records(EVIDENCE_DIR)
    errors: list[str] = []
    for path, record in raw_pairs:
        errors.extend(validate_raw(record, path, signal_set))
    for path, record in evidence_pairs:
        errors.extend(validate_evidence(record, path))

    raw_records = [record for _, record in raw_pairs]
    evidence_records = [record for _, record in evidence_pairs]
    errors.extend(ensure_unique(raw_records))
    evidence_ids = Counter(str(r.get("vacancy_id")) for r in evidence_records)
    errors.extend(f"duplicate evidence vacancy_id: {key}" for key, count in evidence_ids.items() if key and count > 1)
    if errors:
        raise CensusError("\n".join(errors))

    evidence_by_id = {record["vacancy_id"]: record for record in evidence_records}
    canonical: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for raw in raw_records:
        evidence = evidence_by_id.get(raw["vacancy_id"])
        reasons = eligibility_reasons(raw, evidence)
        if reasons:
            rejected.append({"vacancy_id": raw["vacancy_id"], "job_url": raw.get("job_url"), "reasons": reasons})
            continue
        canonical.append(canonicalize(raw, evidence, signal_fields, keywords))

    canonical.sort(key=lambda row: row["vacancy_id"])
    fieldnames = BASE_FIELDS + signal_fields

    report = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "target_population_requested": TARGET_POPULATION,
        "raw_record_count": len(raw_records),
        "evidence_record_count": len(evidence_records),
        "verified_active_exact_title_population": len(canonical),
        "coverage": f"{len(canonical)} / {TARGET_POPULATION}",
        "rejected_count": len(rejected),
        "rejected": rejected,
        "status": "PASS",
    }

    if write_outputs:
        MARKET.mkdir(parents=True, exist_ok=True)
        QUALITY_DIR.mkdir(parents=True, exist_ok=True)
        write_csv(MARKET / "malaysia_finops_engineer_vacancies.csv", canonical, fieldnames)
        (MARKET / "malaysia_finops_engineer_vacancies.json").write_text(json.dumps(canonical, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        write_csv(MARKET / "vacancy_skill_matrix.csv", canonical, ["vacancy_id", "company", "job_title"] + signal_fields)

        for filename, (label, names) in DERIVED_OUTPUTS.items():
            if filename == "finops_capability_frequency.csv":
                names = groups["finops_capability"]
            elif filename == "skill_frequency.csv":
                names = groups["engineering"]
            rows = frequency_rows(canonical, list(names or []), label)
            write_csv(MARKET / filename, rows, [label, "count", "percentage"])

        write_csv(MARKET / "industry_frequency.csv", categorical_frequency(canonical, "industry", "industry"), ["industry", "count", "percentage"])
        write_csv(MARKET / "seniority_frequency.csv", categorical_frequency(canonical, "seniority", "seniority"), ["seniority", "count", "percentage"])
        (QUALITY_DIR / "latest_validation.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (REPO_ROOT / "docs" / "MARKET_ANALYSIS.md").write_text(render_market_analysis(canonical, groups, rejected), encoding="utf-8")

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the Malaysia FinOps Engineer market census")
    parser.add_argument("--validate-only", action="store_true", help="Validate raw/evidence inputs without writing outputs")
    args = parser.parse_args()
    try:
        report = build(write_outputs=not args.validate_only)
    except CensusError as exc:
        print(f"MARKET CENSUS FAILED\n{exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
