from basetest.testcase import SimpleTestCase
from main.models.posts.formats import Formats
from main.views import reverse


class FormatsHtmlTests(SimpleTestCase):
    def test_linkify_hashtags(self):
        plain_text = Formats.postprocess_html("#one #two #three")
        self.assert_html_links_to(plain_text, reverse.tag("one"), displaytext="#one")
        self.assert_html_links_to(plain_text, reverse.tag("two"), displaytext="#two")
        self.assert_html_links_to(
            plain_text, reverse.tag("three"), displaytext="#three"
        )

        html = Formats.postprocess_html(r"<p>#one #two #three</p>")
        self.assert_html_links_to(html, reverse.tag("one"), displaytext="#one")
        self.assert_html_links_to(html, reverse.tag("two"), displaytext="#two")
        self.assert_html_links_to(html, reverse.tag("three"), displaytext="#three")

    def test_prettify_links(self):
        html = (
            "<p>"
            '<a class="keep-this" href="https://github.com/beatonma">https://github.com/beatonma</a> '
            '<a href="https://pypi.org/project/django-wm" id="keep_this_too">https://pypi.org/project/django-wm</a> '
            '<a href="https://reddit.com/r/space">https://reddit.com/r/space</a> '
            '<a href="https://reddit.com/u/fallofmath/">https://reddit.com/u/fallofmath/</a> '
            '<a href="https://www.thingiverse.com/thing:4828770">https://www.thingiverse.com/thing:4828770</a> '
            '<a href="https://youtube.com/@fallofmath">https://youtube.com/@fallofmath</a> '
            '<a href="https://youtube.com/watch?v=blah">https://youtube.com/watch?v=blah</a> '
            '<a href="https://unaffected.url/path?i=blah">https://unaffected.url/path?i=blah</a> '
            '<a href="https://unaffected.url/path?i=blah">Explicit display text is maintained</a> '
            '<a href="http://unaffected.url/path?i=keep-non-https-urls">http://unaffected.url/path?i=keep-non-https-urls</a> '
            "</p>"
        )

        formatted = Formats.postprocess_html(html)
        self.assert_html_links_to(
            formatted,
            "https://reddit.com/u/fallofmath/",
            displaytext="/u/fallofmath",
        )
        self.assert_html_links_to(
            formatted,
            "https://reddit.com/r/space",
            displaytext="/r/space",
        )
        self.assert_html_links_to(
            formatted,
            "https://youtube.com/@fallofmath",
            displaytext="youtube/@fallofmath",
        )
        self.assert_html_links_to(
            formatted,
            "https://youtube.com/watch?v=blah",
            displaytext="youtube",
        )
        self.assert_html_links_to(
            formatted,
            "https://github.com/beatonma",
            displaytext="github/beatonma",
        )
        self.assert_html_links_to(
            formatted,
            "https://www.thingiverse.com/thing:4828770",
            displaytext="thingiverse/4828770",
        )
        self.assert_html_links_to(
            formatted,
            "https://pypi.org/project/django-wm",
            displaytext="pypi/django-wm",
        )
        self.assert_html_links_to(
            formatted,
            "https://unaffected.url/path?i=blah",
            displaytext="unaffected.url/…",
        )
        self.assert_html_links_to(
            formatted,
            "https://unaffected.url/path?i=blah",
            displaytext="Explicit display text is maintained",
        )
        self.assert_html_links_to(
            formatted,
            "https://unaffected.url/path?i=blah",
            displaytext="Explicit display text is maintained",
        )
        self.assert_html_links_to(
            formatted,
            "http://unaffected.url/path?i=keep-non-https-urls",
            displaytext="http://unaffected.url/path?i=keep-non-https-urls",
        )

        self.assertInHTML(
            '<a href="https://github.com/beatonma" class="keep-this">github/beatonma</a>',
            formatted,
        )
        self.assertInHTML(
            '<a href="https://pypi.org/project/django-wm" id="keep_this_too">pypi/django-wm</a>',
            formatted,
        )


class LinkifyKeywordsTests(SimpleTestCase):
    EXPECTED_LINK = '<a href="https://beatonma.org">beatonma.org</a>'

    def test_simple(self):
        self.assertHTMLEqual(
            Formats.postprocess_html("beatonma.org"),
            self.EXPECTED_LINK,
        )

    def test_replaces_only_first_instance(self):
        self.assertHTMLEqual(
            Formats.postprocess_html("beatonma.org and beatonma.org again"),
            f"{self.EXPECTED_LINK} and beatonma.org again",
        )

    def test_replacement_ignored_when_link_already_in_html(self):
        self.assertHTMLEqual(
            Formats.postprocess_html(
                '<a href="https://beatonma.org">beatonma.org</a> and beatonma.org again'
            ),
            '<a href="https://beatonma.org">beatonma.org</a> and beatonma.org again',
        )

    def test_replace_similar(self):
        self.assert_html_links_to(
            Formats.postprocess_html(
                "docker compose and docker should be different links"
            ),
            {
                "https://github.com/docker/compose",
                "https://www.docker.com",
            },
        )

        self.assertHTMLEqual(
            Formats.postprocess_html("microformat and microformats"),
            """<a href="https://microformats.org">microformat</a> and microformats""",
        )

    def test_replacement_in_text_block(self):
        self.assertHTMLEqual(
            Formats.postprocess_html(
                "This is stuff about beatonma.org and it's super interesting"
            ),
            f"This is stuff about {self.EXPECTED_LINK} and it's super interesting",
        )

        self.assertHTMLEqual(
            Formats.postprocess_html(
                "This is stuff about beatonma.org: it's super interesting"
            ),
            f"This is stuff about {self.EXPECTED_LINK}: it's super interesting",
        )

        self.assertHTMLEqual(
            Formats.postprocess_html("This is stuff about beatonma.org."),
            f"This is stuff about {self.EXPECTED_LINK}.",
        )

        linked = Formats.postprocess_html(
            """This site is powered by Django, Celery, Nginx and PostgreSQL, running as a Docker Compose project on 
            Lightsail.

The front end is built with a mixture of Sass, React and Typescript, preprocessed with Gulp and Webpack.

beatonma.org is built with the Indieweb in mind. It supports Microformats and Webmentions (via my library, django-wm)."""
        )
        self.assert_html_links_to(linked, "https://beatonma.org", "beatonma.org")
        self.assert_html_links_to(
            linked, "https://github.com/docker/compose", "Docker Compose"
        )
        self.assert_html_links_to(
            linked, "https://github.com/beatonma/django-wm", "django-wm"
        )
        self.assert_html_links_to(linked, "https://gulpjs.com", "Gulp")
        self.assert_html_links_to(linked, "https://indieweb.org", "Indieweb")
        self.assert_html_links_to(linked, "https://www.nginx.com", "Nginx")
        self.assert_html_links_to(linked, "https://postgreql.org", "PostgreSQL")
        self.assert_html_links_to(linked, "https://reactjs.org", "React")
        self.assert_html_links_to(linked, "https://sass-lang.com", "Sass")
        self.assert_html_links_to(linked, "https://typescriptlang.org", "Typescript")
        self.assert_html_links_to(linked, "https://webpack.js.org", "Webpack")
