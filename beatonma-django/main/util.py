import logging
import re
from typing import Optional

from bs4 import BeautifulSoup
from django.conf import settings

VIDEO_PATTERN = re.compile(r".*\.(mp4|webm)$")
AUDIO_PATTERN = re.compile(r".*\.(mp3)$")

log = logging.getLogger(__name__)


def text_from_html(html: str) -> str:
    """Extract raw text from the given html."""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    return "\n".join(chunk for chunk in chunks if chunk)


def get_media_type_description(file: Optional["RelatedFile"]) -> str:
    if not file:
        return ""

    if VIDEO_PATTERN.match(file.file.url):
        return "video"
    elif AUDIO_PATTERN.match(file.file.url):
        return "audio"
    else:
        return "image"


def to_absolute_url(path: str) -> str:
    return f"https://{settings.DOMAIN_NAME}{path}"
