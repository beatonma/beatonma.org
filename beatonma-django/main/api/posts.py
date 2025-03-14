from datetime import datetime
from typing import Annotated

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from main.models import Post
from main.models.related_file import MediaType
from main.util import to_absolute_url
from main.views.querysets import get_main_feed
from ninja import Field, Router, Schema
from ninja.pagination import paginate
from pydantic import AfterValidator, BeforeValidator

router = Router(tags=["Posts"])

# TODO 98 items in feed

type AbsoluteUrl = Annotated[str, AfterValidator(to_absolute_url)]


class Theme(Schema):
    color_muted: str | None = None
    color_vibrant: str | None = None


class Image(Schema):
    url: AbsoluteUrl = Field(alias="thumbnail_or_none.url")
    type: MediaType
    description: str | None


type ImageOrNone = Annotated[
    Image | None, BeforeValidator(lambda x: x if x and x.thumbnail else None)
]


class File(Schema):
    url: AbsoluteUrl = Field(alias="file_or_none.url")
    type: MediaType
    description: str | None


class Link(Schema):
    url: str
    description: str | None = None
    host: str | None = Field(alias="host.name", default=None)
    icon: AbsoluteUrl | None = Field(alias="host.icon_file", default=None)


class App(Schema):
    title: str
    url: str = Field(alias="get_absolute_url")


class PostPreview(Schema):
    title: str | None
    preview_text: str | None
    url: str | None = Field(alias="get_absolute_url")
    image: ImageOrNone = Field(alias="hero_image", default=None)
    published_at: datetime
    is_published: bool
    content_html: str | None
    app: App | None
    files: list[File] = Field(alias="related_files", default_factory=list)
    links: list[Link] = Field(default_factory=list)


class PostDetail(Schema):
    title: str | None
    subtitle: str | None = None
    url: str | None = Field(alias="get_absolute_url")
    hero_image: ImageOrNone
    hero_html: str | None
    published_at: datetime
    is_published: bool
    content_html: str | None
    app: App | None
    files: list[File] = Field(alias="related_files", default_factory=list)
    links: list[Link] = Field(default_factory=list)


@router.get("/", response=list[PostPreview])
@paginate
def post_feed(request: HttpRequest):
    return Post.objects.all()
    # return get_main_feed()


@router.get("/{slug}/", response=PostDetail)
def post_feed(request: HttpRequest, slug: str):
    return get_object_or_404(Post, slug=slug)
