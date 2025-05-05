import re
import uuid
from typing import Literal

from bs4 import BeautifulSoup

from common.models import BaseModel, PublishedMixin, TaggableMixin
from common.models.api import ApiEditable
from common.models.cache import InvalidateCacheMixin
from common.models.published import PublishedQuerySet
from common.util import regex
from common.util.pipeline import PipelineItem
from django.db import models
from django.db.models import Manager
from django.urls import reverse
from main.models.formats import FormatMixin, Formats
from main.models.link import LinkedMixin
from main.models.mixins import ThemeableMixin
from main.models.related_file import RelatedFilesMixin
from mentions.models.mixins import MentionableMixin

type PostType = Literal["post", "app", "changelog"]


class PostQuerySet(PublishedQuerySet):
    pass


class BasePost(
    InvalidateCacheMixin,
    PublishedMixin,
    MentionableMixin,
    TaggableMixin,
    LinkedMixin,
    RelatedFilesMixin,
    ThemeableMixin,
    FormatMixin,
    ApiEditable,
    BaseModel,
):
    class Meta:
        abstract = True
        ordering = ("-published_at",)

    cache_key = "__post__"

    search_enabled = True
    search_fields = ("title", "content", "tags__name")

    objects = PostQuerySet.as_manager()

    # At least one of the listed fields must have useful content before publishing.
    publishing_require_field = (
        "title",
        "content",
        "related_files",
    )

    hero_image = models.OneToOneField(
        "UploadedFile",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    hero_html = models.TextField(
        blank=True,
        null=True,
    )
    hero_embedded_url = models.URLField(blank=True, null=True)

    slug = models.SlugField(unique=True, max_length=255, editable=True, blank=True)
    old_slug = models.SlugField(unique=True, max_length=255, editable=False, null=True)

    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)

    preview = models.CharField(max_length=512, blank=True, null=True)
    preview_html = models.TextField(blank=True, null=True, editable=False)

    content = models.TextField(blank=True, null=True)
    content_html = models.TextField(blank=True, null=True, editable=False)

    content_script = models.TextField(blank=True, null=True)

    def save_text(self):
        if not self.content:
            self.content = ""

        self.content_html = Formats.to_html(
            self.content,
            self.format,
            markdown_processors=self.extra_markdown_processors(),
            html_processors=self.extra_html_processors(),
        )

        if not self.preview:
            self.preview = ""

        self.preview_html = Formats.to_html(
            self.preview,
            markdown_processors=self.extra_markdown_processors(),
            html_processors=self.extra_html_processors(),
        )

    def extra_markdown_processors(self) -> list[PipelineItem[str]]:
        return []

    def extra_html_processors(self) -> list[PipelineItem[BeautifulSoup]]:
        return []

    def save(self, *args, update_fields=None, **kwargs):
        if not self.slug:
            self.slug = self.build_slug()

        self.save_text()

        if (
            update_fields
            and "content" in update_fields
            and "content_html" not in update_fields
        ):
            update_fields = [*update_fields, "content_html"]

        self.is_published = self.is_published and self.is_publishable()

        super().save(*args, update_fields=update_fields, **kwargs)

        self._extract_tags()

    def is_publishable(self) -> bool:
        return self._has_required_field() and super().is_publishable()

    def _has_required_field(self):
        for field in self.publishing_require_field:
            value = getattr(self, field)
            if isinstance(value, str) and value.strip():
                return True
            if isinstance(value, Manager) and value.count() > 0:
                return True

        return False

    def get_content_html(self) -> str:
        return self.content_html

    def build_slug(self):
        return f"{self.published_at.strftime("%Y%m%d")}{uuid.uuid4().hex[:3]}"

    def get_absolute_url(self) -> str:
        return reverse(self.qualified_name(), kwargs={"slug": self.slug})

    @classmethod
    def resolve_from_url_kwargs(cls, slug: str):
        return cls.objects.get(slug=slug)

    def get_mentions(self):
        sources = set()
        from_unique_sources = []
        mentions = super().get_mentions()
        for m in mentions:
            if m.source_url not in sources:
                sources.add(m.source_url)
                from_unique_sources.append(m)

        return from_unique_sources

    def _extract_tags(self):
        """Generate tags from any #hashtags found in the text."""
        matches = [m.groupdict() for m in re.finditer(regex.HASHTAG, self.content)]
        tags = [x["name"] for x in matches]
        self.tags.add(*tags)

    def __str__(self):
        return (
            f"{self.__class__.__name__}: {self.title or self.content[:64] or self.slug}"
        )


class Post(BasePost):
    pass
