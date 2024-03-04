import logging
import re
from typing import Optional
from urllib.parse import urljoin

from django.conf import settings

VIDEO_PATTERN = re.compile(r".*\.(mp4|webm)$")
AUDIO_PATTERN = re.compile(r".*\.(mp3|wav)$")
IMAGE_PATTERN = re.compile(r".*\.(jpe?g|png|svg|webp)$")
TEXT_PATTERN = re.compile(r".*\.(md|txt)$")

log = logging.getLogger(__name__)


def get_media_type_description(file: Optional["RelatedFile"]) -> str:
    if not file:
        return ""

    url = file.file.url
    if VIDEO_PATTERN.match(url):
        return "video"
    if AUDIO_PATTERN.match(url):
        return "audio"
    if IMAGE_PATTERN.match(url):
        return "image"
    if TEXT_PATTERN.match(url):
        return "text"
    return "unknown"


def to_absolute_url(path: str) -> str:
    return urljoin(f"https://{settings.DOMAIN_NAME}", path)
