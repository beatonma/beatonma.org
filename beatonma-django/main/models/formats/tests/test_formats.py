from main.models.formats.tests import BaseFormatsTestCase


class FormatsTests(BaseFormatsTestCase):
    """Test specific troublesome examples encountered in the wild."""

    def test_sample_links_in_code_block(self):
        markdown = """
```json5

// https://example.org/webmention/get?url=my-article
```
  """
        expected_html = self.codeblock(
            """<span class="c1">// https://example.org/webmention/get?url=my-article</span>"""
        )
        self.assert_md(markdown, expected_html)

    def test_comments_in_code_block(self):
        markdown = """
```html
{% load webmention_endpoint %}
<!-- my-template.html -->

<head>
  <!-- Rendered as <link rel="webmention" href="/webmention/" /> -->
  {% webmention_endpoint %}
</head>
```
"""
        expected_html = self.codeblock(
            """{% load webmention_endpoint %}
<span class="cm">&lt;!-- my-template.html --&gt;</span>

<span class="p">&lt;</span><span class="nt">head</span><span class="p">&gt;</span>
  <span class="cm">&lt;!-- Rendered as &lt;link rel="webmention" href="/webmention/" /&gt; --&gt;</span>
  {% webmention_endpoint %}
<span class="p">&lt;/</span><span class="nt">head</span><span class="p">&gt;</span>"""
        )

        self.assert_md(markdown, expected_html, exact=True)
