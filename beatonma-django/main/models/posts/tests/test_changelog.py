from basetest.testcase import LocalTestCase
from main.models import ChangelogPost


class ChangelogTests(LocalTestCase):
    fixtures = [LocalTestCase.relpath(__file__, "fixtures/changelog.json")]

    def test_changelog_formatting(self):
        cl = ChangelogPost.objects.get(pk=249)
        cl.save()
        cl.refresh_from_db()

        print(cl.content_html)

        self.assert_html_links_to(
            cl.content_html, "https://github.com/beatonma/django-wm/issues/54"
        )
        self.assert_html_links_to(
            cl.content_html,
            "https://github.com/beatonma/django-wm/wiki/Settings#WEBMENTIONS_DOMAINS_INCOMING_ALLOW",
        )
