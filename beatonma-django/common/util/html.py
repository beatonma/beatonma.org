"""Copied from django-wm."""

from typing import Set

from bs4 import BeautifulSoup, ResultSet

__all__ = [
    "html_parser",
    "find_links_in_html",
    "find_links_in_soup",
    "text_from_html",
]


def html_parser(content) -> BeautifulSoup:
    return BeautifulSoup(content, features="html5lib")


def find_links_in_html(html: str) -> Set[str]:
    """Get the raw target href of any links in the html."""
    soup = html_parser(html)
    return find_links_in_soup(soup)


def find_links_in_soup(soup: BeautifulSoup) -> set[str]:
    links = soup.find_all("a", href=True)
    return {a["href"] for a in links}


def text_from_html(html: str) -> str:
    """Extract raw text from the given html."""
    soup = html_parser(html)
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    return "\n".join(chunk for chunk in chunks if chunk)
