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

    def test_explicit_open_record_is_verified_bucket(self):
        self.assertEqual(
            MODULE.classify({"status": "open-and-current", "deadline": "2026-11-24"}, self.today),
            "verified",
        )

    def test_registry_window_is_candidate_not_verified(self):
        self.assertEqual(
            MODULE.classify({"status": "official-api-window-current", "deadline": "2026-12-01"}, self.today),
            "candidate",
        )

    def test_expired_deadline_is_excluded(self):
        self.assertEqual(
            MODULE.classify({"status": "open-and-current", "deadline": "2026-11-19"}, self.today),
            "exclude",
        )

    def test_unverified_and_closed_are_excluded(self):
        self.assertEqual(MODULE.classify({"verification_status": "unverified"}, self.today), "exclude")
        self.assertEqual(MODULE.classify({"status": "closed"}, self.today), "exclude")
        self.assertEqual(MODULE.classify({"status": "withdrawn"}, self.today), "exclude")

    def test_missing_status_is_excluded(self):
        self.assertEqual(MODULE.classify({"title": "Unknown"}, self.today), "exclude")


class ReportTests(unittest.TestCase):
    def test_report_keeps_candidate_distinct(self):
        records = [
            {"country_code": "CL", "title_hu": "Nyitott program", "status": "open-and-current",
             "deadline": "2026-11-24", "official_url": "https://example.org/open"},
            {"country_code": "ES", "title_original": "Registry candidate",
             "status": "official-api-window-current", "deadline": "2026-12-01",
             "official_url": "https://example.org/candidate"},
            {"country_code": "FR", "title": "Unverified", "verification_status": "unverified"},
        ]
        output = MODULE.render(records, date(2026, 11, 20))
        self.assertIn("Kifejezetten nyitottként jelzett lehetőségek", output)
        self.assertIn("Ellenőrzendő nyilvántartási jelöltek", output)
        self.assertIn("Nyitott program", output)
        self.assertIn("Registry candidate", output)
        self.assertNotIn("Unverified", output)

    def test_loader_reads_only_record_objects_from_discovery_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "demo-discovery.json").write_text(
                json.dumps({"generated_at": "2026-11-20T00:00:00Z",
                            "records": [{"id": "a"}, "not-a-record"]}),
                encoding="utf-8",
            )
            (folder / "bad-discovery.json").write_text("{invalid", encoding="utf-8")
            records = MODULE.load_records(folder)
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["id"], "a")
            self.assertEqual(records[0]["_dataset"], "demo-discovery.json")


if __name__ == "__main__":
    unittest.main(verbosity=2)
