import unittest
from unittest.mock import patch
import urllib.error

from scripts.discover_hu_nkfih import fetch_page


class NKFIHRetryTests(unittest.TestCase):
    @patch("scripts.discover_hu_nkfih.time.sleep")
    @patch("scripts.discover_hu_nkfih.urllib.request.urlopen")
    def test_retries_temporary_network_failure_then_succeeds(self, urlopen, sleep):
        class Response:
            headers = {}
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self): return b"<html>ok</html>"
        urlopen.side_effect = [urllib.error.URLError("temporary timeout"), Response()]
        self.assertEqual(fetch_page(object(), attempts=3), "<html>ok</html>")
        self.assertEqual(urlopen.call_count, 2)
        sleep.assert_called_once_with(1)

    @patch("scripts.discover_hu_nkfih.time.sleep")
    @patch("scripts.discover_hu_nkfih.urllib.request.urlopen")
    def test_does_not_retry_permanent_unauthorized_response(self, urlopen, sleep):
        error = urllib.error.HTTPError("https://nkfih.gov.hu", 401, "Unauthorized", {}, None)
        urlopen.side_effect = error
        with self.assertRaises(urllib.error.HTTPError):
            fetch_page(object(), attempts=3)
        self.assertEqual(urlopen.call_count, 1)
        sleep.assert_not_called()

    @patch("scripts.discover_hu_nkfih.time.sleep")
    @patch("scripts.discover_hu_nkfih.urllib.request.urlopen")
    def test_retries_temporary_server_error(self, urlopen, sleep):
        class Response:
            headers = {}
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self): return b"ok"
        error = urllib.error.HTTPError("https://nkfih.gov.hu", 503, "Unavailable", {}, None)
        urlopen.side_effect = [error, Response()]
        self.assertEqual(fetch_page(object(), attempts=2), "ok")
        self.assertEqual(urlopen.call_count, 2)
        sleep.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
