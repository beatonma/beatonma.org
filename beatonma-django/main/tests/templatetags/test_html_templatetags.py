from unittest import TestCase

from main.templatetags.html import notetext


class HtmlTemplateTagTests(TestCase):
    def test_notetext(self):
        self.assertEqual("simple text", notetext("simple text"))
        self.assertEqual(
            "text with embedded tags",
            notetext(
                """text with <span class="some-class">embedded</span> <div id="id">tags</div>"""
            ),
        )
        self.assertEqual(
            """text with embedded tags and a <a href="https://example.com/">link</a>""",
            notetext(
                """text with <span class="some-class">embedded</span> <div id="id">tags</div> and a <a href="https://example.com/">link</a>"""
            ),
        )

        self.assertEqual(
            """text with embedded tags and a <a href="https://example.com/">link</a>""",
            notetext(
                """text with <span class="some-class">embedded</span> <div id="id">tags</div> and a <a href="https://example.com/">link</a><link title="self-closing tag should be removed" />"""
            ),
        )
