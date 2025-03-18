from datetime import datetime

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from main.models import Post
from main.models.mixins import ThemeableMixin
from main.models.related_file import BaseUploadedFile, MediaType
from main.views.querysets import get_main_feed
from ninja import Field, Router, Schema
from ninja.pagination import paginate

router = Router(tags=["Posts"])

# TODO 98 items in feed

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


class App(Schema):
    title: str
    url: str = Field(alias="get_absolute_url")


class BasePost(Schema):
    title: str | None
    url: str | None = Field(alias="get_absolute_url")
    is_published: bool
    published_at: datetime
    theme: Theme | None = None
    app: App | None
    files: list[File] = Field(alias="related_files", default_factory=list)
    links: list[Link] = Field(default_factory=list)
    hero_image: File | None
    content_html: str | None
    links: list[Link]
    files: list[File]

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
    subtitle: str | None = None
    hero_html: str | None


@router.get("/", response=list[PostPreview])
@paginate
def post_feed(request: HttpRequest, query: str = None):
    return Post.objects.all()
    # return get_main_feed()


@router.get("/{slug}/", response=PostDetail)
def post(request: HttpRequest, slug: str):
    return get_object_or_404(Post, slug=slug)
