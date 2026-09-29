import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "python" / "market_census" / "build_market_census.py"
spec = importlib.util.spec_from_file_location("market_census", MODULE_PATH)
market_census = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(market_census)


class MarketCensusUnitTests(unittest.TestCase):
    def test_exact_title_phrase_accepts_supported_titles(self):
        self.assertTrue(market_census.TITLE_RE.search("FinOps Engineer"))
        self.assertTrue(market_census.TITLE_RE.search("Senior FinOps Engineer"))
        self.assertTrue(market_census.TITLE_RE.search("FinOps Engineer II"))

    def test_exact_title_phrase_rejects_related_titles(self):
        self.assertFalse(market_census.TITLE_RE.search("FinOps Analyst"))
        self.assertFalse(market_census.TITLE_RE.search("Cloud Cost Engineer"))
        self.assertFalse(market_census.TITLE_RE.search("Cloud Financial Management Analyst"))

    def test_keyword_classifier_and_manual_override(self):
        taxonomy = {
            "cloud": {"aws": ["aws"], "azure": ["azure"], "gcp": ["gcp"]},
            "engineering": {"python": ["python"]},
        }
        fields, keywords, _ = market_census.flatten_taxonomy(taxonomy)
        record = {
            "role_summary": "Build Python automation across AWS and Azure.",
            "responsibility_text": "",
            "requirement_text": "",
            "preferred_text": "",
            "manual_overrides": {"python": False},
        }
        signals = market_census.classify(record, fields, keywords)
        self.assertTrue(signals["aws"])
        self.assertTrue(signals["azure"])
        self.assertTrue(signals["multi_cloud"])
        self.assertFalse(signals["python"])

    def test_eligibility_requires_evidence(self):
        raw = {
            "active_status": True,
            "job_title": "FinOps Engineer",
            "job_url": "https://example.com/job/1",
            "source": "Example",
        }
        self.assertEqual(market_census.eligibility_reasons(raw, None), ["missing_evidence"])

    def test_eligibility_rejects_location_without_verification(self):
        raw = {
            "active_status": True,
            "job_title": "FinOps Engineer",
            "job_url": "https://example.com/job/1",
            "source": "Example",
        }
        evidence = {
            "active_status": True,
            "title_verified": True,
            "malaysia_verified": False,
            "job_url": "https://example.com/job/1",
            "source": "Example",
        }
        self.assertIn("malaysia_not_verified", market_census.eligibility_reasons(raw, evidence))

    def test_duplicate_url_is_rejected(self):
        rows = [
            {"vacancy_id": "MY-FE-0001", "job_url": "https://example.com/a"},
            {"vacancy_id": "MY-FE-0002", "job_url": "https://example.com/a"},
        ]
        errors = market_census.ensure_unique(rows)
        self.assertIn("duplicate job_url: https://example.com/a", errors)

    def test_frequency_uses_verified_population_denominator(self):
        rows = [{"aws": True}, {"aws": False}, {"aws": True}, {"aws": False}]
        result = market_census.frequency_rows(rows, ["aws"], "cloud")
        self.assertEqual(result[0]["count"], 2)
        self.assertEqual(result[0]["percentage"], 50.0)


if __name__ == "__main__":
    unittest.main()
