import tempfile
import unittest
from pathlib import Path
from scripts.validate_sitemap import validate_sitemap

BASE = "https://example.test/project/"

class SitemapValidationTests(unittest.TestCase):
    def test_valid_existing_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "index.html").write_text("ok", encoding="utf-8")
            xml = f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{BASE}</loc></url></urlset>'
            self.assertEqual(validate_sitemap(xml, Path(tmp), BASE), [])

    def test_missing_page_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            xml = f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{BASE}missing.html</loc></url></urlset>'
            self.assertTrue(any("Missing local page" in e for e in validate_sitemap(xml, Path(tmp), BASE)))

    def test_duplicate_url_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "index.html").write_text("ok", encoding="utf-8")
            xml = f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{BASE}</loc></url><url><loc>{BASE}</loc></url></urlset>'
            self.assertTrue(any("Duplicate URL" in e for e in validate_sitemap(xml, Path(tmp), BASE)))

    def test_external_url_is_rejected(self):
        xml = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://other.test/</loc></url></urlset>'
        self.assertTrue(any("outside expected site" in e for e in validate_sitemap(xml, Path("."), BASE)))

    def test_malformed_xml_is_reported(self):
        self.assertTrue(validate_sitemap("<urlset>"))

if __name__ == "__main__":
    unittest.main()
