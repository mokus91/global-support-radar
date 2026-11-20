import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path

from check_beta_data_quality import audit, valid_https_url


class BetaDataQualityTests(unittest.TestCase):
    def test_https_url_validation(self):
        self.assertTrue(valid_https_url("https://example.gov/funding"))
        self.assertFalse(valid_https_url("http://example.gov"))
        self.assertFalse(valid_https_url("https://user:pass@example.gov"))

    def test_read_only_audit_flags_duplicates_stale_and_overdue_without_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = {
                "feeds": [{
                    "file": "sample.json",
                    "checked_at": "2026-11-15T00:00:00Z",
                    "status": "checked",
                    "records_count": 2
                }]
            }
            payload = {"records": [
                {"id": "same", "title": "One", "official_url": "https://example.gov/one", "deadline": "2026-11-01"},
                {"id": "same", "title": "Two", "official_url": "http://example.gov/two", "deadline": "2026-11-02"}
            ]}
            (root / "feed-status.json").write_text(json.dumps(manifest), encoding="utf-8")
            feed_path = root / "sample.json"
            original = json.dumps(payload)
            feed_path.write_text(original, encoding="utf-8")
            report = audit(root, now=dt.datetime(2026, 11, 20, tzinfo=dt.timezone.utc))
            self.assertEqual(report["duplicate_ids"], 1)
            self.assertEqual(report["invalid_urls"], 1)
            self.assertEqual(report["overdue_deadlines"], 2)
            self.assertEqual(report["stale_feeds"], 1)
            self.assertEqual(feed_path.read_text(encoding="utf-8"), original)

    def test_missing_feed_is_error_not_silent_deletion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "feed-status.json").write_text(json.dumps({"feeds": [{
                "file": "gone.json", "checked_at": "2026-11-20T00:00:00Z",
                "status": "missing", "records_count": 0
            }]}), encoding="utf-8")
            report = audit(root, now=dt.datetime(2026, 11, 20, tzinfo=dt.timezone.utc))
            self.assertTrue(any("file missing" in item for item in report["feed_errors"]))


if __name__ == "__main__":
    unittest.main()
