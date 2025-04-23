import logging
import re

from common.models import BaseModel, PublishedMixin, TaggableMixin
from common.models.api import ApiEditable
from common.models.search import SearchResult
from common.util import regex
from common.util.html import text_from_html
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.text import slugify
from main.models.formats import FormatMixin, Formats
from main.models.posts.app import Link
from main.models.related_file import RelatedFilesMixin
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

    def save(self, *args, update_fields=None, **kwargs):
        if not self.slug:
            self.slug = self.build_slug()

        self.save_text()

        if (
            update_fields
            and "content" in update_fields
            and "content_html" not in update_fields
        ):
            # Ensure that saving `content` field also updates saved value for `content_html`.
            update_fields = [*update_fields, "content_html"]

        super().save(*args, update_fields=update_fields, **kwargs)

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

    def get_content_html(self):
        return self.content_html

    def raw_text(self):
        return text_from_html(self.get_content_html())

    def to_search_result(self) -> SearchResult:
        return SearchResult(
            name=self.content,
            url=self.get_absolute_url(),
            timestamp=self.published_at,
        )

    def _extract_tags(self):
        """Generate tags from any #hashtags found in the text."""
        matches = [m.groupdict() for m in re.finditer(regex.HASHTAG, self.content)]
        tags = [x["name"] for x in matches]
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
                autopreview += "…"
            self.preview_text = autopreview

        self.content_html = Formats.to_html(self.format, self.content)

    def build_slug(self):
        return slugify(f'{self.created_at.strftime("%y%m%d")}-{self.title}')

    def get_content_html(self):
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
