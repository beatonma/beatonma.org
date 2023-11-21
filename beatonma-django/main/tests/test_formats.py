from basetest.testcase import LocalTestCase
from common.util.html import html_parser
from main.models.posts import formats
from main.models.posts.formats import Formats, _linkify_keywords
from main.views import reverse


class LinkifyHashtagTests(LocalTestCase):
    def test_linkify_hashtags(self):
        plain_text = formats._linkify_hashtags("#one #two #three")
        self.assert_html_links_to(plain_text, reverse.tag("one"), displaytext="#one")
        self.assert_html_links_to(plain_text, reverse.tag("two"), displaytext="#two")
        self.assert_html_links_to(
            plain_text, reverse.tag("three"), displaytext="#three"
        )

        html = formats._linkify_hashtags(r"<p>#one #two #three</p>")
        self.assert_html_links_to(html, reverse.tag("one"), displaytext="#one")
        self.assert_html_links_to(html, reverse.tag("two"), displaytext="#two")
        self.assert_html_links_to(html, reverse.tag("three"), displaytext="#three")


class PrettifyLinkTests(LocalTestCase):
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

        formatted = formats._prettify_links(html)
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

    def test_md_link_patterns(self):
        """Tests for patterns passed to markdown2 link-patterns extra."""

        formatted = Formats.to_html(
            Formats.MARKDOWN,
            "This is text with links to /u/fallofmath and /r/android "
            "and github/beatonma and pypi/django-wm and thingiverse/4828770 "
            "and thing/4828771 and youtube/@fallofmath amd youtube/fallofmath2 "
            "and https://google.com and https://www.google.com/search?q=test",
        )

        self.assert_html_links_to(
            formatted,
            "https://reddit.com/u/fallofmath",
            displaytext="/u/fallofmath",
        )
        self.assert_html_links_to(
            formatted,
            "https://reddit.com/r/android",
            displaytext="/r/android",
        )
        self.assert_html_links_to(
            formatted,
            "https://github.com/beatonma",
            displaytext="github/beatonma",
        )
        self.assert_html_links_to(
            formatted,
            "https://thingiverse.com/thing:4828770",
            displaytext="thingiverse/4828770",
        )
        self.assert_html_links_to(
            formatted,
            "https://youtube.com/@fallofmath",
            displaytext="youtube/@fallofmath",
        )
        self.assert_html_links_to(
            formatted,
            "https://youtube.com/@fallofmath2",
        )
        self.assert_html_links_to(
            formatted,
            "https://google.com",
            displaytext="google.com/…",
        )
        self.assert_html_links_to(
            formatted,
            "https://www.google.com/search?q=test",
            displaytext="google.com/…",
        )


class LinkifyKeywordsTests(LocalTestCase):
    EXPECTED_LINK = '<a href="https://beatonma.org">beatonma.org</a>'

    def test_simple(self):
        self.assertEqual(
            _linkify_keywords("beatonma.org"),
            self.EXPECTED_LINK,
        )

    def test_replaces_only_first_instance(self):
        self.assertEqual(
            _linkify_keywords("beatonma.org and beatonma.org again"),
            f"{self.EXPECTED_LINK} and beatonma.org again",
        )

    def test_does_not_match_already_linkified(self):
        self.assertEqual(
            _linkify_keywords(
                '<a href="https://beatonma.org">beatonma.org</a> and beatonma.org again'
            ),
            f"{self.EXPECTED_LINK} and {self.EXPECTED_LINK} again",
        )

    def test_replacement_in_text_block(self):
        self.assertEqual(
            _linkify_keywords(
                "This is stuff about beatonma.org and it's super interesting"
            ),
            f"This is stuff about {self.EXPECTED_LINK} and it's super interesting",
        )

        self.assertEqual(
            _linkify_keywords(
                "This is stuff about beatonma.org: it's super interesting"
            ),
            f"This is stuff about {self.EXPECTED_LINK}: it's super interesting",
        )

        self.assertEqual(
            _linkify_keywords("This is stuff about beatonma.org."),
            f"This is stuff about {self.EXPECTED_LINK}.",
        )


class LigatureTests(LocalTestCase):
    def test_simple_text_ligatures(self):
        self.assertEqual(
            formats._apply_ligatures("if this(c) -> that..."),
            "if this&copy; &rarr; that&hellip;",
        )

    def test_code_blocks_unchanged(self):
        code_blocks = [
            "```foo() -> bar```",
            "`foo() -> bar`",
            "`foo() -> bar` and `foo() -> bar`",
            "```foo() -> bar```",
            """```python
def func(*args) -> str:
    return "ok"
```
""",
        ]
        for block in code_blocks:
            self.assertEqual(formats._apply_ligatures(block), block)

    def test_ligatures_in_mixed_content(self):
        mixed_content = """
Here's some text with -> and (c) ligatures.
This is a code block:
```
def foo():
    return x -> y
```
Another code ==> `block...`:
```python
x = 10
y = 20
z = x (c) y
```
"""

        self.assertEqual(
            formats._apply_ligatures(mixed_content),
            """
Here's some text with &rarr; and &copy; ligatures.
This is a code block:
```
def foo():
    return x -> y
```
Another code &xrArr; `block...`:
```python
x = 10
y = 20
z = x (c) y
```
""",
        )

    def test_individual_ligatures(self):
        for key, value in formats._LIGATURES.items():
            self.assertEqual(formats._apply_ligatures(key), value)


class FormatsTests(LocalTestCase):
    def assert_md(self, content: str, expected: str):
        actual = html_parser(Formats.to_html(Formats.MARKDOWN, content)).prettify()
        expected = html_parser(expected).prettify()
        self.assertEqual(actual, expected)

    def test_markdown_link_formatting(self):
        self.assert_md(
            "something about beatonma.org!",
            '<p>something about <a href="https://beatonma.org">beatonma.org</a>!</p>',
        )
        self.assert_md(
            "something about [beatonma.org](https://beatonma.org)?",
            '<p>something about <a href="https://beatonma.org">beatonma.org</a>?</p>',
        )

    def test_markdown_complex(self):
        self.assert_md(
            """# Article

This --> is a #complicated piece of writing with a link(tm) to beatonma.org and some `inline code` and...

```python

# And a block of code
```

## Another section

| Table |
|-------|
|content|

List of stuff:
- one(r)
- two(c)
- ==> three
""",
            """<h1 id="article">Article</h1>

<p>This &xrarr; is a <a href="/tag/complicated/">#complicated</a> piece of writing with a link&trade; to <a href="https://beatonma.org">beatonma.org</a> and some <code>inline code</code> and&hellip;</p>

<div class="codehilite">
<pre><span></span><code><span class="c1"># And a block of code</span>
</pre></code>
</div>

<h2 id="another-section">Another section</h2>

<table>
<thead><tr><th>Table</th></tr></thead>
<tbody><tr><td>content</td></tr></tbody>
</table>

<p>List of stuff:</p>

<ul>
<li>one®</li>
<li>two©</li>
<li>&xrArr; three</li></ul>""",
        )
