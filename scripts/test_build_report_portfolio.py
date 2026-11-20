import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from build_report_portfolio import build_portfolio, load_profiles


class PortfolioTests(unittest.TestCase):
    def test_generates_one_report_per_profile_with_filters(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = root / "data"
            data.mkdir()
            (data / "sample-discovery.json").write_text(json.dumps({
                "generated_at": "2026-11-20T09:00:00Z",
                "records": [
                    {"title": "HU Business", "country": "HU", "category": "business",
                     "official_url": "https://example.org/hu", "source_checked_at": "2026-11-20",
                     "status": "open-and-current", "deadline": "2026-12-01"},
                    {"title": "ES Agriculture", "country": "ES", "category": "agriculture",
                     "official_url": "https://example.org/es", "source_checked_at": "2026-11-20",
                     "status": "open-and-current", "deadline": "2026-12-01"}
                ]
            }), encoding="utf-8")
            config = root / "profiles.json"
            config.write_text(json.dumps({"profiles": [
                {"id": "hu-business", "title": "HU business", "country": "HU", "category": "business"},
                {"id": "global-all", "title": "Global", "country": None, "category": None}
            ]}), encoding="utf-8")
            outputs = build_portfolio(data, config, root / "out", today=date(2026, 11, 20))
            self.assertEqual(len(outputs), 2)
            hu = outputs[0].read_text(encoding="utf-8")
            glob = outputs[1].read_text(encoding="utf-8")
            self.assertIn("HU Business", hu)
            self.assertNotIn("ES Agriculture", hu)
            self.assertIn("ES Agriculture", glob)

    def test_rejects_duplicate_and_unsafe_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "profiles.json"
            path.write_text(json.dumps({"profiles": [
                {"id": "same", "country": None, "category": None},
                {"id": "same", "country": None, "category": None}
            ]}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_profiles(path)
            path.write_text(json.dumps({"profiles": [
                {"id": "../escape", "country": None, "category": None}
            ]}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_profiles(path)


if __name__ == "__main__":
    unittest.main()
