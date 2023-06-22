from basetest.testcase import LocalTestCase


class ApiTest(LocalTestCase):
    """Ensure that API endpoints are accessible."""

    def test_ping(self):
        """/ping/ should confirm server is available."""
        self.assert_status_ok("/ping/")
