import re
from re import Match
from typing import List

import markdown2
from common.util import regex
from django.db import models
from main.views import reverse

"""Regex to match a simple HTML <a> with the same href and inner text."""
_HTML_ANCHOR_REGEX = re.compile(
    rf"(<a .*?href=\"(?P<href>https://(?:www\.)?[-.\w]+/[-/@=:?\w]+?)\".*?>)(?P<displaytext>\2)(</a>)"
)
_FRIENDLY_URL_REPLACEMENTS = {
    r"https://(www\.)?(old\.)?reddit\.com/r/(?P<name>[-\w]+)/?": "/r/{name}",
    r"https://(www\.)?(old\.)?reddit\.com/u(ser)?/(?P<name>[-\w]+)/?": "/u/{name}",
    r"https://(www\.)?github\.com/(?P<name>[-\w]+)/?": "github/{name}",
    r"https://(www\.)?pypi\.org/project/(?P<name>[-\w]+)/?": "pypi/{name}",
    r"https://(www\.)?thingiverse\.com/thing:(?P<name>\d+)/?": "thingiverse/{name}",
    r"https://(www\.)?youtube\.com/(?P<name>@[-\w]+)/?": "youtube/{name}",
    r"https://(www\.)?youtube\.com/watch\?v=(?P<name>[-\w]+)/?": "youtube",
}

"""Keys will be replaced with their corresponding value.

Beware: Order matters! If one key is a substring of another it should be defined
later in the dictionary."""
_LIGATURES = {
    "<->": "↔",
    "<-->": "⟷",
    "<=>": "⇔",
    "<==>": "⟺",
    "-->": "⟶",
    "->": "→",
    "<--": "⟵",
    "<-": "←",
    "==>": "⟹",
    "=>": "⇨",
    "<==": "⟸",
    "<=": "⇦",
    "...": "…",
    "(c)": "©",
    "(r)": "®",
    "(tm)": "™",
    " --- ": " — ",
    " -- ": " – ",
}


class Formats(models.IntegerChoices):
    NONE = 0
    MARKDOWN = 1

    @classmethod
    def to_html(cls, format_: int, content: str) -> str:
        if format_ == Formats.MARKDOWN:
            html = _markdown_to_html(_apply_ligatures(content))
        else:
            html = content

        return _postprocess_html(html)


class FormatMixin(models.Model):
    class Meta:
        abstract = True

    format = models.PositiveSmallIntegerField(
        choices=Formats.choices,
        default=Formats.MARKDOWN,
    )


def _url_tag(href: str, displayname: str):
    return f'<a href="{href}">{displayname}</a>'


def _postprocess_html(html: str) -> str:
    return _linkify_hashtags(_friendly_common_links(html))


def _linkify_hashtags(html: str) -> str:
    """Replace raw string #hashtags with a link to that tag."""
    return re.sub(
        regex.HASHTAG,
        lambda match: f"{match.group(1)}{_url_tag(href=reverse.tag(match.group(3)), displayname=match.group(2))}",
        html,
    )


def _friendly_common_links(html: str) -> str:
    """Replace URLs with common domains with a reduced display name."""

    def _sub(match: Match):
        for pattern, replacement in _FRIENDLY_URL_REPLACEMENTS.items():
            pattern_match = re.match(pattern, match.group(2))
            if pattern_match:
                named = replacement.format(name=pattern_match.group("name"))
                return f"{match.group(1)}{named}{match.group(4)}"

        return match.group(0)

    return re.sub(_HTML_ANCHOR_REGEX, _sub, html)


def _apply_ligatures(text: str) -> str:
    marker = "__canonical_code_block__"
    canonical_blocks: List[str] = []

    def remember_canonical(match: Match):
        canonical_blocks.append(match.group())
        return marker

    editable_text = re.sub(
        "(```.*?```|`[^`].*?`)",
        remember_canonical,
        text,
        flags=re.DOTALL,
    )

    for pattern, repl in _LIGATURES.items():
        editable_text = editable_text.replace(pattern, repl)

    editable_text = re.sub(marker, lambda match: canonical_blocks.pop(0), editable_text)

    return editable_text


def _markdown_to_html(content) -> str:
    pattern = (
        r"((([A-Za-z]{3,9}:(?:\/\/)?)"  # scheme
        r"(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+(:\[0-9]+)?"  # user@hostname:port
        r"|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)"  # www.|user@hostname
        r"((?:\/[\+~%\/\.\w\-_]*)?"  # path
        r"\??(?:[\-\+=&;:%@\.\w_]*)"  # query parameters
        r"#?(?:[\.\!\/\\\w]*))?)"  # fragment
        r"(?![^<]*?(?:<\/\w+>|\/?>))"  # ignore anchor HTML tags
        r"(?![^\(]*?\))"  # ignore links in brackets (Markdown links and images)
    )
    link_patterns = [(re.compile(pattern), r"\1")]

    return markdown2.markdown(
        content,
        extras=[
            "fenced-code-blocks",
            "link-patterns",
            "header-ids",
            # "numbering",
            "smarty-pants",
            "spoiler",
            "strike",
            "tables",
            "tag-friendly",
        ],
        link_patterns=link_patterns,
    )
