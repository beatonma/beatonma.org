import re
from re import Match
from typing import Callable, Iterable
from urllib.parse import urljoin

import markdown2
from bs4 import BeautifulSoup, NavigableString, PageElement, Tag
from common.util import regex
from common.util.html import find_links_in_soup, html_parser
from common.util.pipeline import PipelineItem, apply_pipeline
from django.db import models
from main.views import reverse

_NAME = r"(?P<name>@?[-\w]+)"
_URL_PREFIX = r"https://(?:www\.)?"
_PRETTY_URL_REPLACEMENTS: dict[str, str] = {
    rf"{_URL_PREFIX}(?:old\.)?reddit\.com/r/{_NAME}.*": r"/r/\g<name>",
    rf"{_URL_PREFIX}(?:old\.)?reddit\.com/u(?:ser)?/{_NAME}.*": r"/u/\g<name>",
    rf"{_URL_PREFIX}github\.com/{_NAME}.*": r"github/\g<name>",
    rf"{_URL_PREFIX}pypi\.org/project/{_NAME}.*": r"pypi/\g<name>",
    rf"{_URL_PREFIX}thingiverse\.com/thing:(?P<name>\d+).*": r"thingiverse/\g<name>",
    rf"{_URL_PREFIX}youtube\.com/watch\?v={_NAME}.*": r"youtube",
    rf"{_URL_PREFIX}youtube\.com/{_NAME}.*": r"youtube/\g<name>",
    rf"{_URL_PREFIX}(?P<host>.*?)([/?]|$).*": r"\g<host>/…",
}


_LINKIFY_PATTERNS: Iterable[tuple[re.Pattern, str]] = [
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


"""The first matching instance of each of these patterns will be linkified in text.

- Text case is ignored.
- Order matters! If one key is a substring of another it should be defined
  later in the dictionary.
  """
_LINKIFY_KEYWORDS: Iterable[tuple[str, str]] = (
    (r"beatonma\.org", "https://beatonma.org"),
    (r"Celery", "https://docs.celeryq.dev"),
    (r"django-wm", "https://github.com/beatonma/django-wm"),
    (r"Django", "https://www.djangoproject.com"),
    (r"Docker Compose", "https://github.com/docker/compose"),
    (r"Docker", "https://www.docker.com"),
    (r"Gulp", "https://gulpjs.com"),
    (r"Indieweb", "https://indieweb.org"),
    (r"Lightsail", "https://aws.amazon.com/lightsail"),
    (r"Microformats?", "https://microformats.org"),
    (r"NextJS", "https://nextjs.org"),
    (r"NGINX", "https://www.nginx.com"),
    (r"PostgreSQL", "https://postgreql.org"),
    (r"React", "https://reactjs.org"),
    (r"Redis", "https://redis.io"),
    (r"SASS", "https://sass-lang.com"),
    (r"Tailwind( ?css)?", "https://tailwindcss.com"),
    (r"Typescript", "https://typescriptlang.org"),
    (r"Webpack", "https://webpack.js.org"),
    (r"Webmentions?", "https://indieweb.org/Webmention"),
)

"""Keys will be replaced with their corresponding value.

Beware: Order matters! If one key is a substring of another it should be defined
later in the dictionary."""
_LIGATURES: dict[str, str] = {
    "<->": "&harr;",  # ↔
    "<-->": "&xharr;",  # ⟷
    "<=>": "&iff;",  # ⇔
    "<==>": "&xhArr;",  # ⟺
    "-->": "&xrarr;",  # ⟶
    "->": "&rarr;",  # →
    "<--": "&xlarr;",  # ⟵
    "<-": "&larr;",  # ←
    "==>": "&xrArr;",  # ⟹
    "=>": "&#x21E8;",  # ⇨
    "<==": "&xlArr;",  # ⟸
    "<=": "&#x21E6;",  # ⇦
    "...": "&hellip;",  # …
    "(c)": "&copy;",  # ©
    "(r)": "&reg;",  # ®
    "(tm)": "&trade;",  # ™
    " --- ": " &mdash; ",  # —
    " -- ": " &ndash; ",  # –
}


class Formats(models.IntegerChoices):
    NONE = 0
    MARKDOWN = 1

    @classmethod
    def to_html(
        cls,
        format_: int,
        content: str,
        markdown_processors: list[PipelineItem[str]] = None,
        html_processors: list[PipelineItem[BeautifulSoup]] = None,
    ) -> str:
        if format_ == Formats.MARKDOWN:
            html = apply_pipeline(
                content,
                [
                    (
                        cls.preprocess_markdown,
                        [],
                        {"pipeline_extras": markdown_processors or []},
                    ),
                    cls.markdown_to_html,
                ],
            )
        else:
            html = content

        return cls.postprocess_html(html, html_processors)

    @classmethod
    def preprocess_markdown(
        cls,
        markdown: str,
        pipeline_extras: list[PipelineItem[str]] = None,
    ) -> str:
        return apply_pipeline(
            markdown,
            [
                *(pipeline_extras or []),
                _apply_ligatures,
                _apply_blockquote_callout,
            ],
        )

    @classmethod
    def postprocess_html(
        cls,
        html: str,
        pipeline_extras: list[PipelineItem[BeautifulSoup]] = None,
    ) -> str:
        soup = html_parser(html)
        existing_links = find_links_in_soup(soup)

        return apply_pipeline(
            soup,
            [
                *(pipeline_extras or []),
                _prettify_links,
                _linkify_hashtags,
                (_linkify_keywords, [existing_links]),
            ],
        ).body.decode_contents()

    @classmethod
    def markdown_to_html(cls, content: str) -> str:
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


class FormatMixin(models.Model):
    class Meta:
        abstract = True

    format = models.PositiveSmallIntegerField(
        choices=Formats.choices,
        default=Formats.MARKDOWN,
    )


def _linkify_hashtags(soup: BeautifulSoup) -> BeautifulSoup:
    def _visit(node: NavigableString):
        if match := re.search(regex.HASHTAG, node):
            anchor = soup.new_tag("a", href=reverse.tag(match.group("name")))
            anchor.string = match.group("hashtag")
            return [(match.start(), match.end(), anchor)]
        return []

    return linkify_soup(soup, visit_string=_visit)


def _prettify_links(soup: BeautifulSoup) -> BeautifulSoup:
    for node in soup.find_all("a", href=True):
        url = node["href"]
        for child in node.contents:
            changes = None
            if isinstance(child, NavigableString) and child == url:
                for pattern, replacement in _PRETTY_URL_REPLACEMENTS.items():
                    display_text, changes = re.subn(pattern, replacement, url)
                    if changes:
                        child.replace_with(display_text)
                        break
            if changes:
                break

    return soup


def _apply_ligatures(markdown: str) -> str:
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


def _apply_blockquote_callout(markdown: str) -> str:
    """
    Convert Github-style markdown callout to HTML, applying style class from frontend <Callout/> component.>

    > [!WARNING]
    > `python manage.py migrate` required for new fields.
    """

    template = """<div class="template-callout-{level}"><p><strong>{level_title}</strong></p>{content}</div>"""
    pattern = re.compile(r"^\s*> \[!(\w+)].*\n((?:^> .+$\n)*)", flags=re.MULTILINE)

    levels = {
        "warning": "warn",
        "error": "warn",
        "note": "info",
    }

    def _replacer(match: re.Match):
        level = match.group(1).lower()
        level_title = level.capitalize()
        level = levels.get(level) or level

        content = Formats.to_html(
            Formats.MARKDOWN,
            str(
                match.group(2).replace("> ", ""),
            ),
        )

        return template.format(level=level, level_title=level_title, content=content)

    return re.sub(pattern, _replacer, markdown)


def linkify_github_issues(*, repo_url: str, markdown: str) -> str:
    def _sub(match: Match):
        issue = match.group("issue")
        href = urljoin(repo_url, f"issues/{issue}")
        return f'<a href="{href}">#{issue}</a>'

    return re.sub(regex.GITHUB_ISSUE, _sub, markdown)


def _linkify_keywords(
    soup: BeautifulSoup,
    existing_links: set[str],
    replacements: Iterable[tuple[str, str]] = _LINKIFY_KEYWORDS,
) -> BeautifulSoup:
    """
    Linkify the first occurrence of each pattern given in replacements, as long
    as the link is not already in existing_links.
    """
    existing_links = existing_links.copy()

    def _visit(node: NavigableString):
        _replacements: list[InsertLinkAt] = []
        for pattern, url in replacements:
            if url in existing_links:
                continue

            if match := re.search(
                rf"(^|(?<=\s|\())(?P<matched>{pattern})(?=$|[,.;:!?\s)])",
                node,
                re.IGNORECASE,
            ):
                anchor = soup.new_tag("a", href=url)
                anchor.string = match.group("matched")
                existing_links.add(url)
                _replacements.append((match.start(), match.end(), anchor))
        return _replacements

    linkify_soup(
        soup,
        visit_string=_visit,
    )
    return soup


# tuple[replace_start_index, replace_end_index, element_to_insert]
type InsertLinkAt = tuple[int, int, PageElement]


def linkify_soup(
    soup: BeautifulSoup,
    visit_string: Callable[[NavigableString], list[InsertLinkAt]],
):
    def visit_node(node: NavigableString | Tag):
        if node.name is None:
            # visit_string may want to insert more than one link in a node,
            # but we can't make changes to the node while traversing it.
            #
            # visit_string must return a list of changes that it wants to make
            # so they can be applied as a batch after traversal is complete
            changes = visit_string(node)

            new_contents = []
            after = node

            for start, end, element in changes:
                new_contents.append(after[:start])
                new_contents.append(element)
                after = after[end:]
            new_contents.append(after)
            node.replace_with(*new_contents)

        elif node.name == "a":
            # Don't try to add links inside links
            return

        else:
            for child in node.contents:
                visit_node(child)

    visit_node(soup)
    return soup
