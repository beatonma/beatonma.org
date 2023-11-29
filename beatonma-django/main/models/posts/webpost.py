import logging
import re

from common.models import BaseModel, PublishedMixin, TaggableMixin
from common.models.api import ApiEditable
from common.models.search import SearchResult
from common.util import regex
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.text import slugify
from main.models.app import Link
from main.models.posts.formats import FormatMixin, Formats
from main.models.related_file import RelatedFilesMixin
from main.util import text_from_html
from mentions.models.mixins.mentionable import MentionableMixin

log = logging.getLogger(__name__)


class BasePost(
    PublishedMixin,
    MentionableMixin,
    TaggableMixin,
    RelatedFilesMixin,
    ApiEditable,
    BaseModel,
):
    class Meta:
        abstract = True
        ordering = ["-created_at"]

    search_fields = ["content", "tags__name"]

    slug = models.SlugField(unique=True, max_length=255, editable=False)

    content = models.TextField(default="")
    content_html = models.TextField(blank=True, default="", editable=False)

    links = GenericRelation(Link)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.build_slug()

        self.save_text()

        super().save(*args, **kwargs)

        self._extract_tags()

    def save_text(self):
        """Do any processing required to generate text such as content_html."""
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement save_text()"
        )

    def build_slug(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement build_slug()"
        )

    def get_absolute_url(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement get_absolute_url()"
        )

    def all_text(self):
        return self.content_html

    def raw_text(self):
        return text_from_html(self.all_text())

    def to_search_result(self) -> SearchResult:
        return SearchResult(
            name=self.content,
            url=self.get_absolute_url(),
            timestamp=self.published_at,
        )

    def _extract_tags(self):
        """Generate tags from any #hashtags found in the text."""
        matches = re.findall(regex.HASHTAG, self.content)
        tags = [x[2] for x in matches]
        self.tags.add(*tags)

    def __str__(self):
        return self.slug


class RichWebPost(FormatMixin, BasePost):
    """Potential subclasses: articles, blog posts, etc."""

    class Meta:
        abstract = True

    search_fields = ["title", "content", "tags__name"]

    title = models.CharField(max_length=255)
    tagline = models.CharField(
        max_length=140,
        null=True,
        blank=True,
        help_text="Short tagline displayed below title",
    )
    preview_text = models.CharField(
        max_length=255,
        blank=True,
        help_text="Text to display beside links to this post",
    )

    def save_text(self):
        if self.preview_text == "":
            autopreview = text_from_html(self.content_html)[:250]
            if len(autopreview) >= 250:
                autopreview = autopreview + "…"
            self.preview_text = autopreview

        self.content_html = Formats.to_html(self.format, self.content)

    def build_slug(self):
        return slugify(f'{self.created_at.strftime("%y%m%d")}-{self.title}')

    def all_text(self):
        return f"{self.title} {self.content_html}"

    def to_search_result(self) -> SearchResult:
        return SearchResult(
            name=self.title,
            url=self.get_absolute_url(),
            timestamp=self.published_at,
            description=self.preview_text,
        )

    def __str__(self):
        return self.slug
