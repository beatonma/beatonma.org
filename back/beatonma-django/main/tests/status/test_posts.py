from basetest.testcase import LocalTestCase
from common.models import PageView
from main.tasks import sample_data


class WebpostViewTests(LocalTestCase):
    """Ensure each webpost type:
    - is accessible
    - renders necessary content
    - renders necessary content on index page
    """

    def test_article(self):
        title = "target title"
        tagline = "tagline"
        preview = "preview text"
        content = "article content"

        article = sample_data.create_article(
            title=title,
            tagline=tagline,
            preview_text=preview,
            content=content,
        )

        self.assert_has_content(article.get_absolute_url(), title, tagline, content)
        self.assert_has_content("/", title, preview)
        self.assert_exists(PageView, url__endswith=article.get_absolute_url())

    def test_blog(self):
        title = "target title"
        tagline = "tagline"
        preview = "preview text"
        content = "blog content"

        blog = sample_data.create_blog(
            title=title,
            tagline=tagline,
            preview_text=preview,
            content=content,
        )

        self.assert_has_content(blog.get_absolute_url(), title, tagline, content)
        self.assert_has_content("/", title, preview)
        self.assert_exists(PageView, url__endswith=blog.get_absolute_url())

    def test_note(self):
        content = "note content"

        note = sample_data.create_note(content=content)

        self.assert_has_content(note.get_absolute_url(), content)
        self.assert_exists(PageView, url__endswith=note.get_absolute_url())

    def test_changelog(self):
        app_name = "Sample app"
        app_version = "1.1"
        changelog_content = "changelog content"
        preview = "preview text"

        app = sample_data.create_app(title=app_name)
        changelog = sample_data.create_changelog(
            app=app,
            version_name=app_version,
            preview_text=preview,
            content=changelog_content,
        )

        self.assert_has_content(
            app.get_absolute_url(),
            app_name,
            app_version,
            changelog_content,
        )
        self.assert_exists(PageView, url__endswith=app.get_absolute_url())

        self.assert_has_content(
            changelog.get_absolute_url(),
            app_name,
            app_version,
            changelog_content,
        )

        self.assert_has_content("/", app_name, app_version, preview)

    def test_about(self):
        content = "about content"
        sample_data.create_about_page(content=content)

        self.assert_has_content("/about/", content)
