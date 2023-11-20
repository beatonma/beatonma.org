import re
from re import Match
from typing import List

import markdown2
from common.util import regex
from django.db import models
from main.views import reverse

_NAME = r"(?P<name>@?[-\w]+)"
_URL_PREFIX = r"https://(?:www\.)?"
_PRETTY_URL_REPLACEMENTS = {
    rf"{_URL_PREFIX}(?:old\.)?reddit\.com/r/{_NAME}.*": r"/r/\g<name>",
    rf"{_URL_PREFIX}(?:old\.)?reddit\.com/u(?:ser)?/{_NAME}.*": r"/u/\g<name>",
    rf"{_URL_PREFIX}github\.com/{_NAME}.*": r"github/\g<name>",
    rf"{_URL_PREFIX}pypi\.org/project/{_NAME}.*": r"pypi/\g<name>",
    rf"{_URL_PREFIX}thingiverse\.com/thing:(?P<name>\d+).*": r"thingiverse/\g<name>",
    rf"{_URL_PREFIX}youtube\.com/watch\?v={_NAME}.*": r"youtube",
    rf"{_URL_PREFIX}youtube\.com/{_NAME}.*": r"youtube/\g<name>",
    rf"{_URL_PREFIX}(?P<host>.*?)([/?]|$).*": r"\g<host>/…",
}


_LINKIFY_PATTERNS = [
    (re.compile(rf"/u/({_NAME})"), r"https://reddit.com/u/\g<name>"),
    (re.compile(rf"/r/({_NAME})"), r"https://reddit.com/r/\g<name>"),
    (re.compile(rf"github/({_NAME})"), r"https://github.com/\g<name>"),
    (re.compile(rf"pypi/({_NAME})"), r"https://pypi.org/project/\g<name>"),
    (
        re.compile(r"thingiverse/(?P<id>\d+)"),
        r"https://thingiverse.com/thing:\g<id>",
    ),
    (re.compile(rf"youtube/@?({_NAME})"), r"https://youtube.com/@\g<name>"),
    (
        re.compile(
            r"((([A-Za-z]{3,9}:(?://)?)"  # scheme
            r"(?:[\-;:&=+$,\w]+@)?[A-Za-z0-9.\-]+(:\[0-9]+)?"  # user@hostname:port
            r"|(?:www\.|[\-;:&=+$,\w]+@)[A-Za-z0-9.\-]+)"  # www.|user@hostname
            r"((?:/[+~%/.\w\-_]*)?"  # path
            r"\??(?:[\-+=&;:%@.\w_]*)"  # query parameters
            r"#?(?:[.!/\\\w]*))?)"  # fragment
            r"(?![^<]*?(?:</\w+>|/?>))"  # ignore anchor HTML tags
            r"(?![^(]*?\))"  # ignore links in brackets (Markdown links and images)
        ),
        r"\1",
    ),  # plaintext URLs
]

_LINKIFY_KEYWORDS = (
    ("beatonma.org", "https://beatonma.org"),
    ("Celery", "https://docs.celeryq.dev"),
    ("Django", "https://www.djangoproject.com"),
    ("Gulp", "https://gulpjs.com"),
    ("Indieweb", "https://indieweb.org"),
    ("Lightsail", "https://aws.amazon.com/lightsail"),
    ("Microformats", "https://microformats.org"),
    ("NGINX", "https://www.nginx.com"),
    ("PostgreSQL", "https://postgreql.org"),
    ("React", "https://reactjs.org"),
    ("SASS", "https://sass-lang.com"),
    ("Typescript", "https://typescriptlang.org"),
    ("Webpack", "https://webpack.js.org"),
    ("Webmention", "https://indieweb.org/Webmention"),
    ("django-wm", "https://github.com/beatonma/django-wm"),
)

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

        return _postprocess_html(html).strip()


class FormatMixin(models.Model):
    class Meta:
        abstract = True

    format = models.PositiveSmallIntegerField(
        choices=Formats.choices,
        default=Formats.MARKDOWN,
    )


def _postprocess_html(html: str) -> str:
    return _linkify_keywords(_linkify_hashtags(_prettify_links(html)))


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
                display_text, changes = re.subn(pattern, replacement, url)
                if changes:
                    break

        return rf"<a {attrs}>{display_text}</a>"

    return re.sub(
        r"<a(?P<attrs_1>.*?)href=\"(?P<url>[^\"]+)\"(?P<attrs_2>.*?)>(?P<display_text>.*?)</a>",
        _sub,
        html,
    )


def _linkify_keywords(html: str) -> str:
    # for match, url in _LINKIFY_KEYWORDS.items():
    for match, url in _LINKIFY_KEYWORDS:
        html = re.sub(
            rf"(^|\s){match}(?=$|[,.;:!?\s])",
            rf'\1<a href="{url}">{match}</a>',
            html,
            count=1,
        )
    return html


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


def _markdown_to_html(content: str) -> str:
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
        link_patterns=_LINKIFY_PATTERNS,
    )
