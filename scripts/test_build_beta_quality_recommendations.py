import importlib.util
import unittest

MODULE_PATH = __import__("pathlib").Path(__file__).with_name("build_beta_quality_recommendations.py")
SPEC = importlib.util.spec_from_file_location("beta_recommendations", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BetaRecommendationTests(unittest.TestCase):
    def test_prioritizes_errors_and_data_integrity_issues(self):
        report = {"feed_errors": ["missing feed"], "invalid_urls": 2, "missing_urls": 1,
                  "duplicate_ids": 3, "missing_titles": 0, "overdue_deadlines": 4,
                  "stale_feeds": 1, "warnings": ["old feed"], "feeds_checked": 2,
                  "records_checked": 10}
        tasks = MODULE.recommendations(report)
        self.assertEqual(tasks[0]["priority"], "P0")
        self.assertEqual(tasks[1]["key"], "invalid_urls")
        self.assertEqual(tasks[3]["count"], 3)

    def test_empty_report_creates_manual_sample_task(self):
        tasks = MODULE.recommendations({})
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["key"], "manual_sample")

    def test_markdown_explicitly_states_read_only_behavior(self):
        rendered = MODULE.render_markdown({"warnings": [], "feed_errors": []})
        self.assertIn("Nem módosít, nem töröl", rendered)
        self.assertIn("Mintavételes kézi ellenőrzés", rendered)


if __name__ == "__main__":
    unittest.main()
