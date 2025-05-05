"""Keys will be replaced with their corresponding value.

Beware: Order matters! If one key is a substring of another it should be defined
later in the dictionary."""

import re
from re import Match
from urllib.parse import urljoin

from common.util import regex

_LIGATURES: dict[str, str] = {
    " <-> ": " &harr; ",  # ↔
    " <--> ": " &xharr; ",  # ⟷
    " <=> ": " &iff; ",  # ⇔
    " <==> ": " &xhArr; ",  # ⟺
    " --> ": " &xrarr; ",  # ⟶
    " -> ": " &rarr; ",  # →
    " <-- ": " &xlarr; ",  # ⟵
    " <- ": " &larr; ",  # ←
    " ==> ": " &xrArr; ",  # ⟹
    " => ": " &#x21E8; ",  # ⇨
    " <== ": " &xlArr; ",  # ⟸
    " <= ": " &#x21E6; ",  # ⇦
    "...": "&hellip;",  # …
    "(c)": "&copy;",  # ©
    "(r)": "&reg;",  # ®
    "(tm)": "&trade;",  # ™
    " --- ": " &mdash; ",  # —
    " -- ": " &ndash; ",  # –
}


def apply_ligatures(markdown: str) -> str:
    marker = "__canonical_code_block__"
    canonical_blocks: list[str] = []

    def remember_canonical(match: Match):
        canonical_blocks.append(match.group())
        return marker

    editable_text = re.sub(
        "(```.*?```|`[^`].*?`)",  # ```code blocks``` or `inline code`
        remember_canonical,
        markdown,
        flags=re.DOTALL,
    )

    for pattern, repl in _LIGATURES.items():
        editable_text = editable_text.replace(pattern, repl)

    editable_text = re.sub(marker, lambda match: canonical_blocks.pop(0), editable_text)

    return editable_text


def apply_blockquote_callout(markdown: str) -> str:
    """
    Convert Github-style markdown callout to HTML, applying style class from frontend <Callout/> component.>

    > [!WARNING]
    > `python manage.py migrate` required for new fields.
    """
    from main.models.formats import Formats

    template = """<div class="template-callout-{level}"><p><strong>{title}</strong></p>{content}</div>"""
    pattern = re.compile(
        r"^> \[!(?P<level>\w+)(?:\|(?P<title>.*?))?]\s*$(?P<content>(?:\n^> .*?$)*)",
        flags=re.MULTILINE,
    )

    levels = {
        "warning": "warn",
        "error": "warn",
        "note": "info",
    }

    def _replacer(match: re.Match):
        level = match.group("level").lower()
        title = match.group("title") or level.capitalize()
        level = levels.get(level) or level

        content = Formats.to_html(
            str(match.group("content").replace("> ", "")),
            Formats.MARKDOWN,
        )

        return template.format(level=level, title=title, content=content)

    return re.sub(pattern, _replacer, markdown)
