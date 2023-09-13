"""Ensure that main site pages are accessible by anonymous users."""
from basetest.testcase import TemplateTestCase


class IndexTest(TemplateTestCase):
    """Ensure main index pages are accessible."""

    def test_main_index(self):
        self.assert_status_ok("/")

    def test_app_index(self):
        self.assert_status_ok("/apps/")


class SearchTest(TemplateTestCase):
    """Ensure search/filter results are accessible."""

    def test_search(self):
        self.assert_status_ok("/search/?query=blah")

    def test_tags(self):
        self.assert_has_content("/tag/art/", "#art")
