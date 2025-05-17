from unittest.mock import patch

import navigation
from basetest.testcase import LocalTestCase
from django.core.cache import cache
from main.models import Post
from main.tasks import sample_data


class WebpostHashtagTests(LocalTestCase):
    def setUp(self) -> None:
        sample_data.create_post(
            title="note",
            content="#startoftext This post has an #awesome-hashtag. "
            "But#not-this-one #yes-this-one",
        )

        sample_data.create_post(
            title="Markdown blog",
            content="#start #middle but not#this-one",
        )

        sample_data.create_post(
            title="HTML blog",
            content="#start #middle but not#this-one",
        )

        sample_data.create_post(
            title="Another markdown blog",
            content="[link to a fragment](https://example.org/article#section) #real",
        )

        sample_data.create_post(
            title="Another HTML blog",
            content="<style>"
            "body { background-color: #f00; } "
            "#target { background-color: #f0f0f0; }}"
            "</style>"
            '<div id="target>this is an #actual-tag</div>',
        )

    def test_tags_are_extracted_from_content(self):
        self.assertListEqual(
            Post.objects.get(title="note").get_tags_list(),
            ["awesome-hashtag", "startoftext", "yes-this-one"],
        )
        self.assertListEqual(
            Post.objects.get(title="Markdown blog").get_tags_list(),
            ["middle", "start"],
        )

    def test_only_tags_are_extracted_from_content(self):
        markdown = Post.objects.get(title="Another markdown blog")
        self.assertListEqual(markdown.get_tags_list(), ["real"])

        html = Post.objects.get(title="Another HTML blog")
        self.assertListEqual(html.get_tags_list(), ["actual-tag"])

    def test_tags_are_linked_in_content_html(self):
        note = Post.objects.get(title="note")
        self.assert_html_links_to(
            note.content_html,
            navigation.tag("awesome-hashtag"),
            displaytext="#awesome-hashtag",
        )
        self.assert_html_links_to(
            note.content_html,
            navigation.tag("startoftext"),
            displaytext="#startoftext",
        )
        self.assert_html_links_to(
            note.content_html,
            navigation.tag("yes-this-one"),
            displaytext="#yes-this-one",
        )

        blog_markdown = Post.objects.get(title="Markdown blog")
        blog_html = Post.objects.get(title="HTML blog")

        for blog in [blog_markdown, blog_html]:
            self.assert_html_links_to(
                blog.content_html,
                navigation.tag("middle"),
                displaytext="#middle",
            )
            self.assert_html_links_to(
                blog.content_html,
                navigation.tag("start"),
                displaytext="#start",
            )

    def test_raw_urls_are_linkified(self):
        note = sample_data.create_post(
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
            displaytext="youtube",
        )

    def test_cache_invalidation(self):
        with patch.object(cache, "delete_pattern") as f:
            Post.objects.filter(title="note").update(title="NOTE")
            f.assert_called_once()

        with patch.object(cache, "delete_pattern") as f:
            Post.objects.filter(title="note").delete()
            f.assert_called_once()
