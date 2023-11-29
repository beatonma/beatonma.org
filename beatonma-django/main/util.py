import logging
import re
from functools import reduce
from typing import Callable, Dict, List, Optional, Tuple, TypeVar, Union
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from django.conf import settings

VIDEO_PATTERN = re.compile(r".*\.(mp4|webm)$")
AUDIO_PATTERN = re.compile(r".*\.(mp3|wav)$")
IMAGE_PATTERN = re.compile(r".*\.(jpe?g|png|svg|webp)$")
TEXT_PATTERN = re.compile(r".*\.(md|txt)$")

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


_T = TypeVar("_T")
_PipelineFunc = Callable[[_T, ...], _T]
_PipelineItem = Union[
    _PipelineFunc,
    Tuple[_PipelineFunc],
    Tuple[_PipelineFunc, List],
    Tuple[_PipelineFunc, List, Dict],
]
_Pipeline = List[_PipelineItem]


def apply_pipeline(receiver: _T, pipeline: _Pipeline) -> _T:
    """Apply each function from the pipeline to the receiver and return the final result."""

    def pipeline_item(accumulator: _T, item: _PipelineItem) -> _T:
        if callable(item):
            return item(accumulator)

        item_len = len(item)
        func = item[0]
        args = item[1] if item_len > 1 else []
        kwargs = item[2] if item_len > 2 else {}

        return func(accumulator, *args, **kwargs)

    return reduce(pipeline_item, pipeline, receiver)
