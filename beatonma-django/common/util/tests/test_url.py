from basetest.testcase import SimpleTestCase
from common.util.url import enforce_trailing_slash


class UrlTests(SimpleTestCase):
    def _assert(self, url, expected):
        self.assertEqual(enforce_trailing_slash(url), expected)

    def test_enforce_trailing_slash(self):
        self._assert("https://beatonma.org", "https://beatonma.org/")
        self._assert("https://beatonma.org/", "https://beatonma.org/")
        self._assert("https://beatonma.org/path", "https://beatonma.org/path/")

        self._assert(
            "https://beatonma.org/path?query=test",
            "https://beatonma.org/path/?query=test",
        )
        self._assert("path?query=test", "path/?query=test")
