import navigation
from main.models.formats import Formats
from main.models.formats.tests import BaseFormatsTestCase


class MarkdownFormatsTest(BaseFormatsTestCase):
    def test_comments_are_maintained(self):
        self.assert_md("<!-- comment -->", "<!-- comment -->")
        self.assert_md(
            """<!-- this is a comment -->This is content<!-- this is a comment -->""",
            "<!-- this is a comment --><p>This is content</p><!-- this is a comment -->",
        )

    def test_useful_whitespace_is_maintained(self):
        expected_html = """<p><a href="#1">link</a> <a href="#2">link</a></p>"""
        formatted = self.assert_md(
            """[link](#1) [link](#2)""",
            expected_html,
        )
        self.assertEqual(formatted, expected_html)

    def test_empty_is_empty(self):
        self.assert_md("", "", exact=True)
        self.assert_md("      \n \r\n ", "", exact=True)

    def test_callout(self):
        self.assert_md(
            markdown="""> [!WARNING]
> `python manage.py migrate` required for new fields.  

- Added `has_been_read: bool` field.  """,
            expected_html="""<div class="template-callout-warn"><p><strong>Warning</strong></p><p><code>python manage.py 
migrate</code> required for new fields.</p></div>
<ul><li>Added <code>has_been_read: bool</code> field.</li></ul>
""",
        )

        self.assert_md(
            markdown="""> [!Important|Custom title]
> Within months...
> 
> The MonoSynth...""",
            expected_html="""<div class="template-callout-important"><p><strong>Custom title</strong></p>
<p>Within months…</p>
<p>The MonoSynth…</p>
</div>
        """,
        )

    def test_markdown(self):
        markdown = """This site uses Django, PostgreSQL, Celery and Redis on the back end. The front end is build with NextJS, Typescript, React and Tailwind. Nginx and Docker Compose tie it all together.

beatonma.org is built with the indieweb in mind. It supports microformats and webmentions (via my django library, django-wm).

beatonma.org is hosted on a VPS in the UK by a European company.
"""

        self.assert_md(
            markdown,
            """<p>This site uses <a href="https://www.djangoproject.com">Django</a>, 
        <a href="https://postgreql.org">PostgreSQL</a>, 
        <a href="https://docs.celeryq.dev">Celery</a> and <a href="https://redis.io">Redis</a> on the back end. The 
        front end is build with <a href="https://nextjs.org">NextJS</a>, <a href="https://typescriptlang.org">Typescript</a>, <a href="https://reactjs.org">React</a> and <a 
        href="https://tailwindcss.com">Tailwind</a>. 
        <a href="https://www.nginx.com">Nginx</a> and <a href="https://github.com/docker/compose">Docker Compose</a> 
        tie it all together.</p>

<p><a href="https://beatonma.org">beatonma.org</a> is built with the <a href="https://indieweb.org">indieweb</a> in 
mind. It supports <a href="https://microformats.org">microformats</a> 
and <a href="https://indieweb.org/Webmention">webmentions</a> (via my django 
library, <a href="https://github.com/beatonma/django-wm">django-wm</a>).</p>

<p>beatonma.org is hosted on a VPS in the UK by a European company.</p>
""",
        )

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

    def test_linkify_hashtags(self):
        html = self.format_markdown("#one #two #three")

        self.assert_html_links_to(html, navigation.tag("one"), displaytext="#one")
        self.assert_html_links_to(html, navigation.tag("two"), displaytext="#two")
        self.assert_html_links_to(html, navigation.tag("three"), displaytext="#three")

    def test_markdown_complex(self):
        markdown = """<!-- comment #1 --># Article
<!-- comment #2 -->
This --> is a #complicated piece of writing with a link(tm) to beatonma.org and some `inline code` and...

```python

# And a block of code
```

## Another section

| Table |
|-------|
|content|
<!-- comment #3 -->

List of stuff:
- one(r)
- two(c)
- ==> three
<!-- comment #4 -->"""
        expected_html = """<!-- comment #1 --><h1 id="article">Article</h1>
<!-- comment #2 -->
<p>This &xrarr; is a <a href="/?tag=complicated">#complicated</a> piece of writing with a link&trade; to <a
href="https://beatonma.org">beatonma.org</a> and some <code>inline code</code> and&hellip;</p>

<div class="codehilite">
<pre>
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
<!-- comment #3 -->
<p>List of stuff:</p>
<ul>
  <li>one®</li>
  <li>two©</li>
  <li>&xrArr; three</li>
</ul>
<!-- comment #4 -->"""
        formatted = self.assert_md(markdown, expected_html)
        self.assertIn("<!-- comment #1 -->", formatted)
        self.assertIn("<!-- comment #2 -->", formatted)
        self.assertIn("<!-- comment #3 -->", formatted)
        self.assertIn("<!-- comment #4 -->", formatted)

    def test_md_link_patterns(self):
        """Tests for patterns passed to markdown2 link-patterns extra."""

        formatted = self.format_markdown(
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
            displaytext="google.com",
        )
        self.assert_html_links_to(
            formatted,
            "https://www.google.com/search?q=test",
            displaytext="google.com/…",
        )


class MarkdownLigatureTests(BaseFormatsTestCase):
    def test_simple_text_ligatures(self):
        self.assertHTMLEqual(
            Formats._preprocess_markdown("if this(c) -> that..."),
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
            self.assertEqual(Formats._preprocess_markdown(block), block)

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
            Formats._preprocess_markdown(mixed_content),
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
        from main.models.formats.markdown import _LIGATURES

        for key, value in _LIGATURES.items():
            self.assertEqual(Formats._preprocess_markdown(key), value)
