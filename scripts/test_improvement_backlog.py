#!/usr/bin/env python3
"""Regression tests for the evidence-based continuous-improvement backlog."""
import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).with_name("generate_improvement_backlog.py")
SPEC = importlib.util.spec_from_file_location("generate_improvement_backlog", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ImprovementBacklogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.data = Path(self.temp.name)
        self.patch = patch.object(MODULE, "DATA", self.data)
        self.patch.start()

    def tearDown(self):
        self.patch.stop()
        self.temp.cleanup()

    def write_json(self, name, value):
        (self.data / name).write_text(json.dumps(value), encoding="utf-8")

    def run_report(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            MODULE.main()
        return output.getvalue()

    def test_flags_unverified_records_and_unavailable_feed(self):
        self.write_json("quality-report.json", {
            "records_checked": 12,
            "feeds_checked": 2,
            "application_state_tiers": {
                "verified_open": 1,
                "needs_verification": 7
            }
        })
        self.write_json("feed-status.json", {
            "feeds": [{
                "name": "Test API",
                "status": "temporarily-unavailable",
                "http_status": 401
            }]
        })
        report = self.run_report()
        self.assertIn("7 rekord további ellenőrzést igényel", report)
        self.assertIn("Test API", report)
        self.assertIn("HTTP 401", report)
        self.assertIn("nem írhatja át önállóan", report)

    def test_missing_reports_produce_safe_fallback(self):
        report = self.run_report()
        self.assertIn("Következő fejlesztési kör", report)
        self.assertIn("nem automatikus kódmódosítás", report)

    def test_malformed_json_is_ignored_without_crashing(self):
        (self.data / "quality-report.json").write_text("{broken", encoding="utf-8")
        report = self.run_report()
        self.assertIn("Következő fejlesztési kör", report)


if __name__ == "__main__":
    unittest.main()
