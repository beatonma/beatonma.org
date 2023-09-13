from basetest.testcase import LocalTestCase
from main.tasks import sample_data
from main.views.querysets import get_main_feed, get_search_results


class FeedTests(LocalTestCase):
    def test_feed(self):
        sample_data.create_note(is_published=True)
        sample_data.create_article(is_published=True)
        sample_data.create_blog(is_published=True)
        app = sample_data.create_app(is_published=True)
        sample_data.create_changelog(app, is_published=True)

        self.assert_length(get_main_feed(), 5)

    def test_feed_does_not_include_unpublished(self):
        sample_data.create_note(is_published=False)
        sample_data.create_article(is_published=False)
        sample_data.create_blog(is_published=False)
        app = sample_data.create_app(is_published=False)
        sample_data.create_changelog(app, is_published=False)

        self.assert_length(get_main_feed(), 0)

    def test_changelog_for_unpublished_app_is_not_published(self):
        app = sample_data.create_app(is_published=False)
        sample_data.create_changelog(app, is_published=True)

        self.assert_length(get_main_feed(), 0)

    def test_unpublished_changelog_for_published_app(self):
        app = sample_data.create_app(is_published=True)
        sample_data.create_changelog(app, is_published=False)

        self.assert_length(get_main_feed(), 1)
        self.assert_length(get_search_results(app.app_id), 1)
