from basetest.testcase import LocalTestCase
from django.urls import reverse


class StatusTests(LocalTestCase):
    """Ensure that API endpoints are accessible."""

    def test_ping(self):
        self.assert_status_ok(reverse("public_api:ping"))

    def test_whoami(self):
        headers = {
            "HTTP_USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/111.0.0.0 Safari/537.36",
        }
        r = self.client.get(
            reverse("public_api:whoami"),
            **headers,
        )

        data = r.json()
        self.assertEqual(data["ip"], "127.0.0.1")
        self.assertEqual(data["device"], "PC")
        self.assertEqual(data["os"], "Linux")
        self.assertTrue(data["browser"].startswith("Chrome"))
