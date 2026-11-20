"""Regression tests for the organization report generator."""
import importlib.util
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("generate_organization_report.py")
SPEC = importlib.util.spec_from_file_location("organization_report", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ClassificationTests(unittest.TestCase):
    def setUp(self):
        self.today = date(2026, 11, 20)
        self.base = {"country_code": "HU", "official_url": "https://example.org/grant", "source_checked_at": "2026-11-20T09:00:00Z"}

    def test_explicit_open_record_is_verified_bucket(self):
        self.assertEqual(MODULE.classify({**self.base, "status": "open-and-current", "deadline": "2026-11-24"}, self.today), "verified")

    def test_registry_window_is_candidate_not_verified(self):
        self.assertEqual(MODULE.classify({**self.base, "status": "official-api-window-current", "deadline": "2026-12-01"}, self.today), "candidate")

    def test_expired_deadline_is_excluded(self):
        self.assertEqual(MODULE.classify({**self.base, "status": "open-and-current", "deadline": "2026-11-19"}, self.today), "exclude")

    def test_unverified_and_closed_are_excluded(self):
        self.assertEqual(MODULE.classify({**self.base, "verification_status": "unverified"}, self.today), "exclude")
        self.assertEqual(MODULE.classify({**self.base, "status": "closed"}, self.today), "exclude")
        self.assertEqual(MODULE.classify({**self.base, "status": "withdrawn"}, self.today), "exclude")

    def test_closed_secondary_status_overrides_open(self):
        self.assertEqual(MODULE.classify({**self.base, "status": "open", "verification_status": "withdrawn"}, self.today), "exclude")

    def test_invalid_deadline_is_excluded(self):
        self.assertEqual(MODULE.classify({**self.base, "status": "open", "deadline": "not-a-date"}, self.today), "exclude")

    def test_missing_status_is_excluded(self):
        self.assertEqual(MODULE.classify({**self.base, "title": "Unknown"}, self.today), "exclude")

    def test_missing_country_source_or_timestamp_is_excluded(self):
        valid = {**self.base, "status": "open"}
        for broken in (
            {**valid, "country_code": ""},
            {**valid, "official_url": "http://example.org"},
            {**valid, "source_checked_at": "not-a-date"},
        ):
            self.assertEqual(MODULE.classify(broken, self.today), "exclude")


class FilterTests(unittest.TestCase):
    def test_country_and_category_filters_are_exact_and_case_insensitive(self):
        records = [
            {"country_code": "HU", "categories": ["business", "energy"]},
            {"country_hu": "Magyarország", "category": "Agriculture"},
            {"country_code": "ES", "category": "business-growth"},
        ]
        self.assertEqual(len(MODULE.filter_records(records, country="hu")), 1)
        self.assertEqual(len(MODULE.filter_records(records, country="MAGYARORSZÁG")), 1)
        self.assertEqual(len(MODULE.filter_records(records, category="BUSINESS")), 1)
        self.assertEqual(len(MODULE.filter_records(records, category="business-growth")), 1)
        self.assertEqual(len(MODULE.filter_records(records)), 3)
        self.assertEqual(MODULE.filter_records(records, country="HU", category="energy"), [records[0]])
        self.assertEqual(MODULE.filter_records(records, category="business-gro"), [])


class ReportTests(unittest.TestCase):
    def test_report_keeps_candidate_distinct_and_preserves_zero_amount(self):
        records = [
            {"country_code": "CL", "title_hu": "Nyitott program", "status": "open-and-current",
             "deadline": "2026-11-24", "official_url": "https://example.org/open", "source_checked_at": "2026-11-20T09:00:00Z", "amount_max": 0},
            {"country_code": "ES", "title_original": "Registry candidate",
             "status": "official-api-window-current", "deadline": "2026-12-01",
             "official_url": "https://example.org/candidate", "source_checked_at": "2026-11-20T09:00:00Z"},
            {"country_code": "FR", "title": "Unverified", "verification_status": "unverified"},
        ]
        output = MODULE.render(records, date(2026, 11, 20))
        self.assertIn("Kifejezetten nyitottként jelzett lehetőségek", output)
        self.assertIn("Ellenőrzendő nyilvántartási jelöltek", output)
        self.assertIn("Nyitott program", output)
        self.assertIn("Registry candidate", output)
        self.assertIn("Összeg/keret:** 0", output)
        self.assertNotIn("Unverified", output)

    def test_duplicate_official_urls_are_removed(self):
        records = [
            {"title": "First title", "official_url": "https://example.org/grant"},
            {"title": "Second title", "official_url": "https://example.org/grant/"},
            {"title": "No URL", "country_code": "HU", "deadline": "2026-12-01"},
            {"title": "No URL", "country_code": "HU", "deadline": "2026-12-01"},
        ]
        self.assertEqual(len(MODULE.deduplicate_records(records)), 2)

    def test_report_shows_selected_filters(self):
        output = MODULE.render(
            [{"title": "Example", "status": "open", "country_code": "HU", "category": "business", "official_url": "https://example.org/x", "source_checked_at": "2026-11-20T09:00:00Z"}],
            date(2026, 11, 20), country="HU", category="business"
        )
        self.assertIn("**Országszűrő:** HU", output)
        self.assertIn("**Témaszűrő:** business", output)
        self.assertIn("**Egyedi rekordok száma:** 1", output)

    def test_non_https_source_is_not_rendered_as_official_link(self):
        output = MODULE.render([
            {"title": "Example", "status": "open", "url": "http://example.org"}
        ], date(2026, 11, 20))
        self.assertIn("Kifejezetten nyitottként jelölt rekord: **0**", output)
        self.assertNotIn("http://example.org", output)

    def test_loader_skips_invalid_json_and_non_object_payloads(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "demo-discovery.json").write_text(
                json.dumps({"generated_at": "2026-11-20T00:00:00Z",
                            "records": [{"id": "a"}, "not-a-record"]}), encoding="utf-8")
            (folder / "bad-discovery.json").write_text("{invalid", encoding="utf-8")
            (folder / "list-discovery.json").write_text("[]", encoding="utf-8")
            (folder / "null-discovery.json").write_text("null", encoding="utf-8")
            records = MODULE.load_records(folder)
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["id"], "a")
            self.assertEqual(records[0]["_dataset"], "demo-discovery.json")


if __name__ == "__main__":
    unittest.main(verbosity=2)
