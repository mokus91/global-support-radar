#!/usr/bin/env python3
"""Regression tests for deadline interpretation."""
import datetime as dt
import unittest

from deadline_utils import parse_deadline


class DeadlineParsingTests(unittest.TestCase):
    def test_date_only_deadline_expires_at_end_of_day(self):
        parsed = parse_deadline("2026-11-20")
        self.assertEqual(parsed, dt.datetime(2026, 11, 20, 23, 59, 59, 999999, tzinfo=dt.timezone.utc))

    def test_timestamp_is_normalized_to_utc(self):
        parsed = parse_deadline("2026-11-20T12:00:00+02:00")
        self.assertEqual(parsed, dt.datetime(2026, 11, 20, 10, 0, tzinfo=dt.timezone.utc))

    def test_z_timestamp_is_supported(self):
        parsed = parse_deadline("2026-11-20T10:00:00Z")
        self.assertEqual(parsed, dt.datetime(2026, 11, 20, 10, 0, tzinfo=dt.timezone.utc))

    def test_invalid_or_missing_deadline_is_unknown(self):
        self.assertIsNone(parse_deadline(None))
        self.assertIsNone(parse_deadline("not-a-date"))


if __name__ == "__main__":
    unittest.main()
