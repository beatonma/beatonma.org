from basetest.testcase import LocalTestCase, TemplateTestCase
from main.models import Blog, Note
from main.models.posts.formats import Formats
from main.views import reverse


class WebpostHashtagTests(LocalTestCase):
    def setUp(self) -> None:
        Note.objects.create(
            content="#startoftext This post has an #awesome-hashtag. "
            "But#not-this-one #yes-this-one"
        )

        Blog.objects.create(
            title="Markdown blog",
            content="#start #middle but not#this-one",
            format=Formats.MARKDOWN,
        )

        Blog.objects.create(
            title="HTML blog",
            content="#start #middle but not#this-one",
            format=Formats.NONE,
        )

    def test_tags_are_extracted_from_content(self):
        self.assertListEqual(
            Note.objects.first().get_tags_list(),
            ["awesome-hashtag", "startoftext", "yes-this-one"],
        )
        self.assertListEqual(
            Blog.objects.first().get_tags_list(),
            ["middle", "start"],
        )


class WebpostHashtagViewTests(TemplateTestCase, WebpostHashtagTests):
    def test_tags_are_linked_in_content_html(self):
        note = Note.objects.first()
        self.assert_html_links_to(
            note.content_html,
            reverse.tag("awesome-hashtag"),
            displaytext="#awesome-hashtag",
        )
        self.assert_html_links_to(
            note.content_html,
            reverse.tag("startoftext"),
            displaytext="#startoftext",
        )
        self.assert_html_links_to(
            note.content_html,
            reverse.tag("yes-this-one"),
            displaytext="#yes-this-one",
        )

        blog_markdown = Blog.objects.get(title="Markdown blog")
        blog_html = Blog.objects.get(title="HTML blog")

        for blog in [blog_markdown, blog_html]:
            self.assert_html_links_to(
                blog.content_html,
                reverse.tag("middle"),
                displaytext="#middle",
            )
            self.assert_html_links_to(
                blog.content_html,
                reverse.tag("start"),
                displaytext="#start",
            )


class WebpostViewTests(TemplateTestCase):
    def test_raw_urls_are_linkified(self):
        note = Note.objects.create(
            content="Links to "
            "and https://reddit.com/u/fallofmath/ "
            "and https://pypi.org/project/django-wm/ "
            "and https://youtube.com/watch?v=123456abcde "
            "and https://github.com/beatonma/ "
            "and https://www.thingiverse.com/thing:4828770"
        )

        self.assert_html_links_to(
            note.content_html,
            "https://youtube.com/watch?v=123456abcde",
            displaytext="youtube/v=123456abcde",
        )
