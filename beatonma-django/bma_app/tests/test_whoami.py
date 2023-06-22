from basetest.testcase import BaseTestCase
from django.urls import reverse


class WhoamiTests(BaseTestCase):
    def test_whoami(self):
        headers = {
            "HTTP_USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        }
        r = self.client.get(
            reverse("bma_app_whoami"),
            **headers,
        )

        data = r.json()
        self.assertEqual(data["ip"], "127.0.0.1")
        self.assertEqual(data["device"], "PC")
        self.assertEqual(data["os"], "Linux")
        self.assertTrue(data["browser"].startswith("Chrome"))
