"""Regression tests for the revenue readiness report."""
import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("build_revenue_readiness_report.py")
SPEC = importlib.util.spec_from_file_location("revenue_readiness", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

class RevenueReadinessTests(unittest.TestCase):
    def test_report_shows_actual_pipeline_without_inflating_leads(self):
        report = MODULE.build_report(now=datetime(2026, 11, 20, tzinfo=timezone.utc))
        self.assertIn("Kutatott célpont: 7", report)
        self.assertIn("Fizető ügyfél: 0", report)
        self.assertIn("Pipeline-ban nyilvántartott bevétel: 0 Ft", report)
        self.assertIn("Nincs igazolt fizető ügyfél", report)

    def test_missing_required_asset_and_pipeline_are_flagged(self):
        with tempfile.TemporaryDirectory() as directory:
            report = MODULE.build_report(root=Path(directory))
        self.assertIn("[HIÁNYZIK] Product definition", report)
        self.assertIn("Pipeline állapot: **MISSING**", report)

    def test_pipeline_rejects_contact_without_owner_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data").mkdir()
            data = {"records":[{"id":"x","status":"contacted","contacted":True,"outreach_approved":False,"revenue_huf":0}]}
            (root / MODULE.PIPELINE_PATH).write_text(json.dumps(data), encoding="utf-8")
            result = MODULE.summarize_pipeline(root)
        self.assertEqual(result["state"], "ERROR")
        self.assertTrue(any("Jóváhagyás nélküli" in e for e in result["errors"]))

    def test_revenue_only_counts_verified_paid_customer(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data").mkdir()
            data = {"records":[{"id":"x","status":"paid_customer","contacted":True,"outreach_approved":True,
                "reply_received":True,"pilot":True,"paid_customer":True,"revenue_huf":12500}]}
            (root / MODULE.PIPELINE_PATH).write_text(json.dumps(data), encoding="utf-8")
            result = MODULE.summarize_pipeline(root)
        self.assertEqual(result["state"], "OK")
        self.assertEqual(result["revenue_huf"], 12500)


    def test_pipeline_rejects_status_flag_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data").mkdir()
            data = {"records":[{"id":"x","status":"researched","outreach_approved":True,
                "contacted":False,"reply_received":False,"pilot":False,"paid_customer":False,"revenue_huf":0}]}
            (root / MODULE.PIPELINE_PATH).write_text(json.dumps(data), encoding="utf-8")
            result = MODULE.summarize_pipeline(root)
        self.assertEqual(result["state"], "ERROR")
        self.assertTrue(any("Státusz és eseményjelölők" in e for e in result["errors"]))

    def test_paid_customer_requires_positive_verified_amount(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data").mkdir()
            data = {"records":[{"id":"x","status":"paid_customer","contacted":True,"outreach_approved":True,
                "reply_received":True,"pilot":True,"paid_customer":True,"revenue_huf":0}]}
            (root / MODULE.PIPELINE_PATH).write_text(json.dumps(data), encoding="utf-8")
            result = MODULE.summarize_pipeline(root)
        self.assertEqual(result["state"], "ERROR")

    def test_owner_queue_prioritizes_replies_and_never_claims_outreach(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data").mkdir()
            data = {"records": [
                {"id":"a","organization":"Alpha","status":"researched","next_action":"Kézi ellenőrzés"},
                {"id":"b","organization":"Beta","status":"replied","next_action":"Igény pontosítása"},
                {"id":"c","organization":"Gamma","status":"outreach_approved","next_action":"Előkészített levél ellenőrzése"}
            ]}
            (root / MODULE.PIPELINE_PATH).write_text(json.dumps(data), encoding="utf-8")
            queue = MODULE.build_owner_action_queue(root)
        self.assertIn("Beta", queue[0])
        self.assertIn("IGÉNYVALIDÁLÁS", queue[0])
        self.assertTrue(any("Alpha" in row and "nem engedélyezett" in row for row in queue))
        self.assertTrue(any("nem küld e-mailt" in row for row in queue))

if __name__ == "__main__":
    unittest.main()
