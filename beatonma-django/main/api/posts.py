import logging
from datetime import datetime
from typing import Literal

from common.schema import Mention
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse
from main.models import AppPost, ChangelogPost, Post
from main.models.mixins import ThemeableMixin
from main.models.related_file import BaseUploadedFile, MediaType
from ninja import Field, Router, Schema
from ninja.pagination import paginate

from .querysets import get_feed

log = logging.getLogger(__name__)
router = Router(tags=["Posts"])

type Url = str

class Theme(Schema):
    muted: str | None = None
    vibrant: str | None = None


class File(Schema):
    url: Url = Field(alias="file_or_none.url")
    thumbnail_url: Url = Field(alias="thumbnail_or_none.url", default=None)
    type: MediaType
    name: str | None = Field(alias="original_filename", default=None)
    description: str | None
    fit: BaseUploadedFile.ImageFit | None


class Link(Schema):
    url: str
    description: str | None = None
    host: str | None = Field(alias="host.name", default=None)
    icon: Url | None = Field(alias="host.icon_file", default=None)


class Tag(Schema):
    name: str


type PostType = Literal["post", "app", "changelog"]


class BasePost(Schema):
    post_type: PostType
    title: str | None
    url: str = Field(alias="get_absolute_url")
    is_published: bool
    published_at: datetime
    theme: Theme | None = None
    hero_image: File | None
    content_html: str | None
    content_script: str | None
    links: list[Link]
    files: list[File]
    tags: list[Tag]

    @staticmethod
    def resolve_theme(obj: ThemeableMixin):
        return {
            "muted": obj.color_muted,
            "vibrant": obj.color_vibrant,
        }

    @staticmethod
    def resolve_files(obj):
        return obj.related_files.all().order_by("sort_order")


class PostPreview(BasePost):
    is_preview: bool

    @staticmethod
    def resolve_content_html(obj):
        return obj.preview_text or obj.content_html

    @staticmethod
    def resolve_is_preview(obj):
        return bool(obj.preview_text)


class PostDetail(BasePost):
    post_type: PostType = "post"
    subtitle: str | None = None
    hero_html: str | None
    mentions: list[Mention] = Field(alias="get_mentions")


class ChangelogDetail(PostDetail):
    post_type: PostType = "changelog"
    version: str


class AppDetail(PostDetail):
    post_type: PostType = "app"
    changelog: list[ChangelogDetail] = Field(alias="changelogs")
    icon: str | None
    script: str | None


@router.get("/", response=list[PostPreview])
@paginate
def post_feed(request: HttpRequest, query: str = None, tag: str = None):
    feed = get_feed(query=query, tag=tag)
    for post in feed:
        if isinstance(post, AppPost):
            post.post_type = "app"
        elif isinstance(post, ChangelogPost):
            post.post_type = "changelog"
            post.title = f"{post.app.title} {post.title}"
        else:
            post.post_type = "post"

    return feed


@router.get("/{slug}/", response=PostDetail | AppDetail | ChangelogDetail)
def post(request: HttpRequest, slug: str):
    return get_object_or_404(Post, slug=slug)
