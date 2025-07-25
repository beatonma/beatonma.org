import re
from dataclasses import dataclass
from typing import Callable, Iterable

import navigation
from bs4 import BeautifulSoup, Comment, NavigableString, PageElement
from common.util.html import find_links_in_soup

URL_REGEX = (
    r"((?:(?P<scheme>[a-zA-Z]{3,9}):(?://))"
    r"(?:www.)?(?P<host>(?:[-.\w]+)\.(?:[a-zA-Z]+))"
    r"(?P<path>/[:+~%/.\w\-_]*)?"
    r"(?P<query>\?[\-+=&;:%@.\w]*)?"
    r"(?P<fragment>#[.!/\w\\]*)?)"
)
_NAME = r"(?P<name>@?[-\w]+)"
_URL_PREFIX = r"https://(?:www\.)?"


def _default_prettify_link(match: re.Match) -> str:
    if match.group("scheme") != "https":
        return match.string

    if match.group("path"):
        return f"{match.group("host")}/…"

    return match.group("host")


type RegexReplacement = str | Callable[[re.Match[str]], str]
_PRETTY_URL_REPLACEMENTS: Iterable[tuple[str, RegexReplacement]] = [
    (rf"{_URL_PREFIX}(?:old\.)?reddit\.com/r/{_NAME}.*", r"/r/\g<name>"),
    (rf"{_URL_PREFIX}(?:old\.)?reddit\.com/u(?:ser)?/{_NAME}.*", r"/u/\g<name>"),
    (rf"{_URL_PREFIX}github\.com/{_NAME}.*", r"github/\g<name>"),
    (rf"{_URL_PREFIX}pypi\.org/project/{_NAME}.*", r"pypi/\g<name>"),
    (rf"{_URL_PREFIX}thingiverse\.com/thing:(?P<name>\d+).*", r"thingiverse/\g<name>"),
    (rf"{_URL_PREFIX}youtube\.com/watch\?v={_NAME}.*", r"youtube"),
    (rf"{_URL_PREFIX}youtube\.com/{_NAME}.*", r"youtube/\g<name>"),
    (URL_REGEX, _default_prettify_link),
]


def prettify_links(soup: BeautifulSoup) -> BeautifulSoup:
    for node in soup.find_all("a", href=True):
        url = node["href"]
        for child in node.contents:
            changes = None
            if isinstance(child, NavigableString) and child == url:
                for pattern, replacement in _PRETTY_URL_REPLACEMENTS:
                    display_text, changes = re.subn(pattern, replacement, url)
                    if changes:
                        child.replace_with(display_text)
                        break
            if changes:
                break

    return soup


class LinkifyPattern:
    pattern: str | re.Pattern
    replacement: RegexReplacement
    only_first: bool

    def __init__(
        self,
        pattern: str,
        replacement: RegexReplacement,
        *,
        require_brackets: bool = False,
        only_first: bool = False,
    ):
        if require_brackets:
            self.pattern = re.compile(
                rf"(^|(?<=\s|\())\[(?P<matched>{pattern})](?=$|[,.;:!?\s)])",
                re.IGNORECASE,
            )
        else:
            self.pattern = re.compile(
                rf"(^|(?<=\s|\())\[?(?P<matched>{pattern})]?(?=$|[,.;:!?\s)])",
                re.IGNORECASE,
            )
        self.replacement = replacement
        self.only_first = only_first


def LinkifyWordOrPhrase(
    pattern: str, replacement: RegexReplacement, only_first: bool = False
) -> LinkifyPattern:
    """Linkify matches only if they are wrapped in [square brackets]."""
    return LinkifyPattern(
        pattern, replacement, only_first=only_first, require_brackets=True
    )


type LinkifyPatterns = Iterable[LinkifyPattern]

"""Order matters! Patterns that are defined first have priority over ones defined later."""
_LINKIFY_PATTERNS: LinkifyPatterns = [
    # Profiles
    LinkifyPattern(rf"/u/({_NAME})", r"https://reddit.com/u/\g<name>"),
    LinkifyPattern(rf"/r/({_NAME})", r"https://reddit.com/r/\g<name>"),
    LinkifyPattern(rf"github/({_NAME})", r"https://github.com/\g<name>"),
    LinkifyPattern(rf"pypi/({_NAME})", r"https://pypi.org/project/\g<name>"),
    LinkifyPattern(
        r"thingiverse/(?P<id>\d+)",
        r"https://thingiverse.com/thing:\g<id>",
    ),
    LinkifyPattern(rf"youtube/@?({_NAME})", r"https://youtube.com/@\g<name>"),
    # Tags
    LinkifyPattern(rf"#(?P<tag>[a-zA-Z][-\w]+)", navigation.tag(tag=r"\g<tag>")),
    # keywords
    LinkifyPattern(r"beatonma\.org", "https://beatonma.org", only_first=True),
    LinkifyWordOrPhrase(r"Celery", "https://docs.celeryq.dev"),
    LinkifyWordOrPhrase(r"django-wm", "https://github.com/beatonma/django-wm"),
    LinkifyWordOrPhrase(r"Django", "https://www.djangoproject.com"),
    LinkifyWordOrPhrase(r"Docker Compose", "https://github.com/docker/compose"),
    LinkifyWordOrPhrase(r"Docker", "https://www.docker.com"),
    LinkifyWordOrPhrase(r"Gulp", "https://gulpjs.com"),
    LinkifyWordOrPhrase(r"Indieweb", "https://indieweb.org"),
    LinkifyWordOrPhrase(r"Lightsail", "https://aws.amazon.com/lightsail"),
    LinkifyWordOrPhrase(r"Microformats?", "https://microformats.org"),
    LinkifyWordOrPhrase(r"NextJS", "https://nextjs.org"),
    LinkifyWordOrPhrase(r"NGINX", "https://www.nginx.com"),
    LinkifyWordOrPhrase(r"PostgreSQL", "https://postgreql.org"),
    LinkifyWordOrPhrase(r"React", "https://reactjs.org"),
    LinkifyWordOrPhrase(r"Redis", "https://redis.io"),
    LinkifyWordOrPhrase(r"SASS", "https://sass-lang.com"),
    LinkifyWordOrPhrase(r"Tailwind( ?css)?", "https://tailwindcss.com"),
    LinkifyWordOrPhrase(r"Typescript", "https://typescriptlang.org"),
    LinkifyWordOrPhrase(r"Webpack", "https://webpack.js.org"),
    LinkifyWordOrPhrase(r"Webmentions?", "https://indieweb.org/Webmention"),
    LinkifyPattern(URL_REGEX, r"\g<0>"),  # Raw links
]


@dataclass
class Replacement:
    span: tuple[int, int]
    display_text: str
    url: str
    priority: int
    only_first: bool


def linkify_html(
    soup: BeautifulSoup, patterns: LinkifyPatterns = None
) -> BeautifulSoup:
    """
    Linkifies text within a BeautifulSoup object using provided patterns and replacements.

    Only the first instance of each link
    """
    patterns = patterns or _LINKIFY_PATTERNS
    existing_urls = find_links_in_soup(soup)

    def process_text_node(text_node):
        original_text = text_node.string
        replacements: list[Replacement] = []

        for priority, item in enumerate(patterns):
            for match in re.finditer(item.pattern, original_text):
                replacements.append(
                    Replacement(
                        span=match.span(),
                        display_text=match.group("matched"),
                        url=(
                            item.replacement(match)
                            if callable(item.replacement)
                            else match.expand(item.replacement)
                        ),
                        priority=priority,
                        only_first=item.only_first,
                    )
                )

        # Sort by `(start, priority)`: links are inserted in the order that they
        # appear. If two links overlap, the one with the higher priority (i.e.
        # defined first in patterns) will be used and the lower priority one will
        # be discarded.
        replacements = sorted(replacements, key=lambda rep: (rep.span[0], rep.priority))

        position = 0
        nodes = []
        for replacement in replacements:
            start, end = replacement.span
            url = replacement.url

            if start < position:
                continue
            if (url in existing_urls) and replacement.only_first:
                continue

            nodes.append(original_text[position:start])
            link = soup.new_tag("a", href=url)
            link.string = replacement.display_text
            nodes.append(link)
            existing_urls.add(url)
            position = end

        nodes.append(original_text[position:])
        text_node.replace_with(*nodes)

    def explore_branch(element: PageElement):
        for element in element.contents:
            if isinstance(element, Comment):
                continue
            if element.name in ["head", "script", "style", "a", "code", "pre"]:
                continue

            if isinstance(element, NavigableString):
                process_text_node(element)
                continue

            explore_branch(element)

    explore_branch(soup)

    return soup


def flatten_contents(soup: BeautifulSoup) -> BeautifulSoup:
    """Unwrap the body contents from its html.body wrapper so all contents
    appear at the root level.

    Parsing an HTML fragment into BeautifulSoup usually results in the content
    being wrapped in <html><body> tags, but a <!-- comment --> at the
    start of the fragment can appear as a top-level element instead of being
    wrapped. By unwrapping the body contents we ensure that the structure of
    the soup is the same as the input HTML."""
    soup.html.replace_with(*soup.body.contents)
    return soup


def remove_empty(soup: BeautifulSoup) -> BeautifulSoup:
    if len(soup.contents) == 1:
        child = soup.contents[0]
        if child.get_text() == "-":
            child.replace_with()

    for x in soup.select("p, span"):
        # Remove elements that have no children
        if not x.contents:
            x.replace_with()
            continue

        # Remove elements that only have comments as children
        for child in x.contents:
            if not isinstance(child, Comment):
                break
        else:
            x.replace_with_children()

    return soup
