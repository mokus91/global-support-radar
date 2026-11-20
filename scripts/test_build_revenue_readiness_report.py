"""Regression tests for the revenue readiness report."""
import importlib.util
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("build_revenue_readiness_report.py")
SPEC = importlib.util.spec_from_file_location("revenue_readiness", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class RevenueReadinessTests(unittest.TestCase):
    def test_report_is_explicit_about_open_blockers(self):
        report = MODULE.build_report(now=datetime(2026, 11, 20, tzinfo=timezone.utc))
        self.assertIn("Nincs igazolt fizető ügyfél", report)
        self.assertIn("nem kér és nem tárol", report)
        self.assertIn("Nyereség =", report)

    def test_missing_required_asset_is_flagged(self):
        with tempfile.TemporaryDirectory() as directory:
            report = MODULE.build_report(root=Path(directory))
        self.assertIn("[HIÁNYZIK] Product definition", report)
        self.assertIn("[HIÁNYZIK] Payment and payout safeguards", report)

    def test_existing_required_asset_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "docs/organizational-pilot-spec.md").write_text("pilot", encoding="utf-8")
            report = MODULE.build_report(root=root)
        self.assertIn("[RENDELKEZÉSRE ÁLL] Product definition", report)


if __name__ == "__main__":
    unittest.main()
