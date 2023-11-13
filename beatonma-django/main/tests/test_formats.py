from basetest.testcase import LocalTestCase
from main.models.posts import formats
from main.views import reverse


class FormatsTests(LocalTestCase):
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

    def test_replacements(self):
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


class LigatureTests(LocalTestCase):
    def test_simple_text_ligatures(self):
        self.assertEqual(
            formats._apply_ligatures("if this(c) -> that..."),
            "if this© → that…",
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
Here's some text with → and © ligatures.
This is a code block:
```
def foo():
    return x -> y
```
Another code ⟹ `block...`:
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
