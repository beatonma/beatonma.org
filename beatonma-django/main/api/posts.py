import logging
from datetime import datetime
from typing import Literal

from common.schema import Mention
from common.util.url import enforce_trailing_slash
from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from main.models import AboutPost, AppPost, ChangelogPost, Post
from main.models.mixins import ThemeableMixin
from main.models.posts.post import BasePost as BasePost_Model
from main.models.posts.post import PostType
from ninja import Field, Router, Schema
from ninja.decorators import decorate_view
from ninja.pagination import paginate

from .querysets import get_feed
from .schema import File, Link

log = logging.getLogger(__name__)
router = Router(tags=["Posts"])


class Theme(Schema):
    muted: str | None = None
    vibrant: str | None = None


class Tag(Schema):
    name: str


class BasePost(Schema):
    post_type: PostType
    title: str | None
    url: str
    is_published: bool
    published_at: datetime
    theme: Theme | None = None
    hero_embedded_url: str | None
    hero_image: File | None
    content_html: str | None
    content_script: str | None
    files: list[File]

    @staticmethod
    def resolve_theme(obj: ThemeableMixin):
        if obj.color_muted or obj.color_vibrant:
            return {
                "muted": obj.color_muted,
                "vibrant": obj.color_vibrant,
            }

    @staticmethod
    def resolve_url(obj):
        if obj.post_type == "app":
            return obj.apppost.get_absolute_url()
        if obj.post_type == "changelog":
            return obj.changelogpost.get_absolute_url()
        return obj.get_absolute_url()

    @staticmethod
    def resolve_files(obj):
        return obj.related_files.all().order_by("sort_order")


class PostPreview(BasePost):
    is_preview: bool

    @staticmethod
    def resolve_content_html(obj):
        if obj.preview == "-":
            # Don't show any content, preview or otherwise
            return None
        return obj.preview_html or obj.content_html

    @staticmethod
    def resolve_is_preview(obj):
        return bool(obj.preview_html)


class AppPreview(PostPreview):
    post_type: Literal["app"] = Field("app")
    icon: File | None = None

    @staticmethod
    def resolve_url(obj):
        return obj.apppost.get_absolute_url()


class PostDetail(BasePost):
    post_type: Literal["post"] = Field("post")
    subtitle: str | None = None
    hero_html: str | None
    links: list[Link]
    tags: list[Tag]
    mentions: list[Mention] = Field(alias="get_mentions")

    @staticmethod
    def resolve_url(obj):
        return obj.get_absolute_url()


class AboutPreview(PostPreview):
    post_type: Literal["about"] = Field("about")
    url: str = Field(alias="get_absolute_url")
    path: str


class AboutDetail(PostDetail):
    post_type: Literal["about"] = Field("about")
    path: str
    parent: AboutPreview | None
    siblings: list[AboutPreview]
    children: list[AboutPreview]

    @staticmethod
    def resolve_children(obj):
        return obj.children.published()

    @staticmethod
    def resolve_siblings(obj):
        if obj.parent:
            return obj.parent.children.published().exclude(pk=obj.pk)
        return []


class ChangelogDetail(PostDetail):
    post_type: Literal["changelog"] = Field("changelog")
    app: AppPreview
    version: str

    @staticmethod
    def resolve_url(obj):
        return obj.changelogpost.get_absolute_url()


class AppDetail(PostDetail):
    post_type: Literal["app"] = Field("app")
    hero_html: str | None
    changelog: list[ChangelogDetail] = Field(alias="changelogs")
    icon: File | None
    script: str | None = Field(alias="script.file.url", default=None)
    script_html: str | None
    is_widget: bool = Field(alias="script_is_widget")
    widget_style: str | None

    @staticmethod
    def resolve_url(obj):
        return obj.apppost.get_absolute_url()


@router.get("/posts/{slug}/", response=PostDetail)
def post(request: HttpRequest, slug: str):
    return get_object_or_404(Post, slug=slug)


@router.get("/apps/{slug}/", response=AppDetail)
def app(request: HttpRequest, slug: str):
    return get_object_or_404(AppPost, slug=slug)


@router.get("/changelog/{slug}/", response=ChangelogDetail)
def changelog(request: HttpRequest, slug: str):
    return get_object_or_404(ChangelogPost, slug=slug)


@router.get("/about/", response=AboutDetail)
def about_root(request: HttpRequest):
    about_page = AboutPost.objects.root()

    if about_page:
        return about_page
    raise Http404()


@router.get("/about/{path:path}", response=AboutDetail)
def about(request: HttpRequest, path: str):
    return get_object_or_404(
        AboutPost.objects.published(), path=enforce_trailing_slash(path)
    )


@router.get("/posts/", response=list[PostPreview])
@paginate
@decorate_view(cache_page(60 * 60, key_prefix=BasePost_Model.cache_key))
def post_feed(
    request: HttpRequest,
    query: str = None,
    tag: str = None,
    feed: str = None,
):
    feed = get_feed(query=query, tag=tag, feed=feed)

    return feed
