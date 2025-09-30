import re
from typing import Annotated
from urllib.parse import quote

from django.utils import html
from main.models.mixins.media_upload import MediaType
from main.models.uploads import BaseUploadedFile
from ninja import Field, Schema
from pydantic import AfterValidator

type PlainText = str
type UnsafeHtml = str
type HtmlAttribute = Annotated[str, AfterValidator(html.escape)]
type HexColor = Annotated[str, AfterValidator(_validate_hex_color)]
type Url = Annotated[str, AfterValidator(_validate_url)]
type UrlSearchParams = Annotated[str, AfterValidator(_validate_url_searchparams)]


class File(Schema):
    url: Url = Field(alias="file_or_none.url")
    thumbnail_url: Url = Field(alias="thumbnail_or_none.url", default=None)
    type: MediaType
    name: PlainText | None = Field(alias="original_filename", default=None)
    description: PlainText | None
    fit: BaseUploadedFile.ImageFit | None


class Link(Schema):
    url: Url
    label: PlainText | None = None
    description: PlainText | None = None
    icon: Url | None = Field(alias="host.icon_file", default=None)


def _validate_hex_color(color: str) -> str | None:
    if re.match(r"^#[0-9A-Fa-f]{6}$", color):
        return color
    return None


def _validate_url(url: str) -> str:
    if url.startswith("/") or "://" in url:
        return url
    raise ValueError(f"URL must be absolute, or relative to root (got '{url}')")


def _validate_url_searchparams(params: str) -> str:
    return quote(params, safe="&=")
