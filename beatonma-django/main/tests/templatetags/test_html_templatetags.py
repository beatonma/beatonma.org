from unittest import TestCase

from main.templatetags.page.post import note_text


class HtmlTemplateTagTests(TestCase):
    def test_notetext(self):
        self.assertEqual("simple text", note_text("simple text"))
        self.assertEqual(
            "text with embedded tags",
            note_text(
                """text with <span class="some-class">embedded</span> <div id="id">tags</div>"""
            ),
        )
        self.assertEqual(
            """text with embedded tags and a <a href="https://example.com/">link</a>""",
            note_text(
                """text with <span class="some-class">embedded</span> <div id="id">tags</div> and a <a href="https://example.com/">link</a>"""
            ),
        )

        self.assertEqual(
            """text with embedded tags and a <a href="https://example.com/">link</a>""",
            note_text(
                """text with <span class="some-class">embedded</span> <div id="id">tags</div> and a <a href="https://example.com/">link</a><link title="self-closing tag should be removed" />"""
            ),
        )
