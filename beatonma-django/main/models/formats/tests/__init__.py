from basetest.testcase import SimpleTestCase
from main.models.formats import Formats


class BaseFormatsTestCase(SimpleTestCase):
    def format_html(self, html: str):
        return Formats.to_html(Formats.NONE, html)

    def format_markdown(self, markdown: str):
        return Formats.to_html(Formats.MARKDOWN, markdown)

    def _assert_formatting_is_correct(
        self, formatted_html: str, expected_html: str, exact: bool = False
    ):
        print(f"EXPECTED:\n{expected_html}\n")
        print(f"FORMATTED:\n{formatted_html}\n")

        msg = None
        context_start = 10
        context_end = 20
        for n, char in enumerate(expected_html):
            if formatted_html[n] != char:
                msg = (
                    f"diff at position {n}\n'{formatted_html[n-context_start:n+context_end]}'\n!=\n"
                    f"'{expected_html[n-context_start:n+context_end]}'"
                )
                break
        else:
            if len(formatted_html) != len(expected_html):
                msg = f"formatted HTML is longer, extra='{formatted_html[len(expected_html):]}'"

        self.assertHTMLEqual(formatted_html, expected_html, msg=msg)

        if exact:
            self.assertEqual(
                formatted_html,
                expected_html,
                msg=f"HTML is equivalent but strings are not equal ({msg or 'unknown difference'}).",
            )
        return formatted_html

    def assert_md(self, markdown: str, expected_html: str, exact: bool = False):
        return self._assert_formatting_is_correct(
            Formats.to_html(Formats.MARKDOWN, markdown), expected_html, exact=exact
        )

    def assert_html(self, html: str, expected_html: str, exact: bool = False):
        return self._assert_formatting_is_correct(
            Formats.to_html(Formats.NONE, html), expected_html, exact=exact
        )

    def codeblock(self, children: str) -> str:
        """Expected wrapper structure for formatted ```code blocks```."""
        return f"""<div class="codehilite">
<pre><code>{children}
</code></pre>
</div>
"""
