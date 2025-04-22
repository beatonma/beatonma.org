from basetest.testcase import SimpleTestCase
from main.models.posts.formats import Formats


class LigatureTests(SimpleTestCase):
    def test_simple_text_ligatures(self):
        self.assertHTMLEqual(
            Formats.preprocess_markdown("if this(c) -> that..."),
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
            self.assertEqual(Formats.preprocess_markdown(block), block)

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
            Formats.preprocess_markdown(mixed_content),
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
        from main.models.posts import formats

        for key, value in formats._LIGATURES.items():
            self.assertEqual(Formats.preprocess_markdown(key), value)


class FormatsMarkdownTests(SimpleTestCase):
    def assert_md(self, markdown: str, html: str):
        self.assertHTMLEqual(Formats.to_html(Formats.MARKDOWN, markdown), html)

    def test_markdown_link_formatting(self):
        self.assert_md(
            "something about beatonma.org!",
            '<p>something about <a href="https://beatonma.org">beatonma.org</a>!</p>',
        )
        self.assert_md(
            "something about [beatonma.org](https://beatonma.org)?",
            '<p>something about <a href="https://beatonma.org">beatonma.org</a>?</p>',
        )
        self.assert_md(
            "something about redistributing redis!",
            '<p>something about redistributing <a href="https://redis.io">redis</a>!</p>',
        )
        self.assert_md(
            "NGINX is a thing",
            '<p><a href="https://www.nginx.com">NGINX</a> is a thing</p>',
        )
        self.assert_md(
            "Tailwind",
            '<p><a href="https://tailwindcss.com">Tailwind</a></p>',
        )
        self.assert_md(
            "tailwindcss",
            '<p><a href="https://tailwindcss.com">tailwindcss</a></p>',
        )
        self.assert_md(
            "Tailwind CSS",
            '<p><a href="https://tailwindcss.com">Tailwind CSS</a></p>',
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
<pre>
  <span></span>
  <code>
    <span class="c1"># And a block of code</span>
  </code>
</pre>
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
  <li>&xrArr; three</li>
</ul>""",
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
