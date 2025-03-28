import re
import uuid

from common.models import BaseModel, PublishedMixin, TaggableMixin
from common.models.api import ApiEditable
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Manager
from django.urls import reverse
from django.utils.text import slugify
from main.models import Link
from main.models.mixins import ThemeableMixin
from main.models.posts.formats import FormatMixin, Formats
from main.models.related_file import RelatedFilesMixin
from mentions.models.mixins import MentionableMixin

HASHTAG_REGEX = re.compile(
    r"(?P<previous_token>^|>|\s)(?P<hashtag>#(?![a-fA-F0-9]{3})(?P<name>[-\w]+))(?=$|[\s.!?<])(?!\s*{)"
)


class BasePost(
    PublishedMixin,
    MentionableMixin,
    TaggableMixin,
    RelatedFilesMixin,
    ThemeableMixin,
    FormatMixin,
    ApiEditable,
    BaseModel,
):
    class Meta:
        abstract = True
        ordering = ("-published_at",)

    search_enabled = True
    search_fields = ("title", "content", "tags__name")

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

    slug = models.SlugField(unique=True, max_length=255, editable=False)
    old_slug = models.SlugField(unique=True, max_length=255, editable=False, null=True)

    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    preview_text = models.CharField(max_length=255, blank=True, null=True)

    content = models.TextField(blank=True, null=True)
    content_html = models.TextField(blank=True, null=True, editable=False)

    content_script = models.TextField(blank=True, null=True)

    links = GenericRelation(Link)

    def save_text(self):
        if not self.content:
            self.content = ""
        self.content_html = Formats.to_html(self.format, self.content)

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
        return reverse("post", kwargs={"slug": self.slug})

    def _extract_tags(self):
        """Generate tags from any #hashtags found in the text."""
        matches = re.findall(HASHTAG_REGEX, self.content)
        tags = [x[2] for x in matches]
        self.tags.add(*tags)

    def __str__(self):
        return f"Post: {self.title or self.content[:64] or self.slug}"


class Post(BasePost):
    pass
