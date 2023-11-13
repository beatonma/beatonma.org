import re
from re import Match
from typing import List

import markdown2
from common.util import regex
from django.db import models
from main.views import reverse
from urllib3.exceptions import LocationParseError
from urllib3.util import parse_url

_PRETTY_URL_REPLACEMENTS = {
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


def _postprocess_html(html: str) -> str:
    return _linkify_hashtags(_prettify_links(html))


def _linkify_hashtags(html: str) -> str:
    """Replace raw string #hashtags with a link to that tag."""

    def _sub(sub_match: Match):
        previous_token = sub_match.group("previous_token")
        href = reverse.tag(sub_match.group("name"))
        display_name = sub_match.group("hashtag")

        return f'{previous_token}<a href="{href}">{display_name}</a>'

    return re.sub(regex.HASHTAG, _sub, html)


def _prettify_links(html: str) -> str:
    """Prettify display text for any links in the given HTML.

    Recognised URLs are replaced as defined in _FRIENDLY_URL_REPLACEMENTS.
    Unrecognised URLs are shortened to their hostname.
    Links that already have explicit display text will not be affected.

    URLs that do not use https scheme are kept in their explicitly ugly form.
    """

    def _sub(sub_match: Match):
        url = sub_match.group("url")
        display_text = sub_match.group("display_text")
        attrs = " ".join(
            [
                x.strip()
                for x in [
                    f'href="{url}"',
                    sub_match.group("attrs_1"),
                    sub_match.group("attrs_2"),
                ]
                if x
            ]
        )

        if display_text == url:
            for pattern, replacement in _PRETTY_URL_REPLACEMENTS.items():
                if pattern_match := re.match(pattern, url):
                    display_text = replacement.format(name=pattern_match.group("name"))
                    break
            else:
                try:
                    parsed_url = parse_url(url)
                    if parsed_url.scheme == "https":
                        display_text = f"{parsed_url.host}/…"
                except LocationParseError:
                    pass

        return rf"<a {attrs}>{display_text}</a>"

    return re.sub(
        r"<a(?P<attrs_1>.*?)href=\"(?P<url>[^\"]+)\"(?P<attrs_2>.*?)>(?P<display_text>.*?)</a>",
        _sub,
        html,
    )


def _apply_ligatures(text: str) -> str:
    marker = "__canonical_code_block__"
    canonical_blocks: List[str] = []

    def remember_canonical(match: Match):
        canonical_blocks.append(match.group())
        return marker

    editable_text = re.sub(
        "(```.*?```|`[^`].*?`)",  # ```code blocks``` or `inline code`
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
            "cuddled-lists",
            "fenced-code-blocks",
            "footnotes",
            "header-ids",
            "link-patterns",
            "smarty-pants",
            "spoiler",
            "strike",
            "tables",
            "tag-friendly",
        ],
        link_patterns=link_patterns,
    )
