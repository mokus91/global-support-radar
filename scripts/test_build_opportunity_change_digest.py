import unittest
from build_opportunity_change_digest import build_digest, display_value

class OpportunityChangeDigestTests(unittest.TestCase):
    def test_eu_status_codes_are_human_readable(self):
        self.assertEqual(display_value("status", "31094502"), "Nyitott (Open)")

    def test_changed_deadline_and_status_are_rendered(self):
        digest = build_digest({"generated_at": "2026-11-20T10:00:00Z", "events": [{
            "type": "changed", "feed": "eu-open-calls-discovery.json", "title": "Sample call",
            "before": {"status": "31094501", "deadline": "2026-12-01"},
            "after": {"status": "31094502", "deadline": "2026-12-15"}
        }]})
        self.assertIn("Előzetesen meghirdetett (Forthcoming)", digest)
        self.assertIn("Nyitott (Open)", digest)
        self.assertIn("2026-12-01", digest)
        self.assertIn("2026-12-15", digest)

    def test_removed_record_is_not_called_closed(self):
        digest = build_digest({"events": [{"type": "removed_from_feed", "title": "Removed", "feed": "sample.json"}]})
        self.assertIn("nem jelenti a felhívás lezárását", digest)
        self.assertNotIn("**Esemény:** closed", digest)

    def test_empty_change_log_is_explicit(self):
        self.assertIn("Nincs rögzített változás", build_digest({"events": []}))

if __name__ == "__main__":
    unittest.main()
