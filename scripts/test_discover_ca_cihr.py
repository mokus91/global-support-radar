import unittest

from discover_ca_cihr import parse_upcoming_html


class CIHRParserTests(unittest.TestCase):
    def test_upcoming_and_published_sections_are_distinguished(self):
        html = """
        <h2>Upcoming funding opportunities</h2>
        <a href="/e/54858.html">Notice of Funding Opportunity: Team Grant – GACD 2027</a>
        <h2>Published funding opportunities</h2>
        <a href="/e/54777.html">Notice of Upcoming Funding Opportunity: National Cancer Data Hub Team Grants</a>
        """
        rows = parse_upcoming_html(html)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["source_status"], "planned-announcement-not-open")
        self.assertEqual(rows[1]["source_status"], "official-listing-not-verified-open")
        self.assertTrue(all(row["open_status_verified"] is False for row in rows))
        self.assertTrue(all(row["eligibility_verified"] is False for row in rows))

    def test_external_links_are_rejected(self):
        html = """
        <h2>Upcoming funding opportunities</h2>
        <a href="https://example.com/funding-opportunity">Funding opportunity</a>
        """
        self.assertEqual(parse_upcoming_html(html), [])


if __name__ == "__main__":
    unittest.main()
