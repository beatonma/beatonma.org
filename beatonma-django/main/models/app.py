import logging
from typing import Optional

from common.models import BaseModel, PublishedMixin, TaggableMixin
from common.models.search import SearchResult
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from main.forms import SanitizedFileField
from main.models.link import Link
from main.models.mixins.styleable_svg import StyleableSvgMixin
from main.models.mixins.themeable import ThemeableMixin
from main.models.related_file import RelatedFilesMixin
from main.views import view_names
from mentions.models.mixins.mentionable import MentionableMixin

log = logging.getLogger(__name__)


class AppType(ThemeableMixin, StyleableSvgMixin, BaseModel):
    name = models.CharField(max_length=50, help_text="e.g. Android, web, server...")
    tooltip = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse(view_names.APPS_BY_TYPE, args=[self.name])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class App(
    PublishedMixin,
    MentionableMixin,
    RelatedFilesMixin,
    TaggableMixin,
    ThemeableMixin,
    BaseModel,
):
    STATUS_OPTIONS = (
        ("dev", "In development"),
        ("test", "Public testing"),
        ("public", "Published"),
        ("deprecated", "Deprecated"),
    )

    search_fields = ["title", "description", "app_id", "tags__name"]

    title = models.CharField(max_length=140)
    description = models.TextField(blank=True, null=True)
    app_id = models.CharField(max_length=255, unique=True, help_text="Application ID")
    slug = models.SlugField(unique=True, max_length=255)
    tagline = models.CharField(max_length=140, blank=True)

    icon = SanitizedFileField(
        blank=True,
        upload_to="app/",
        size=[800, 800],
    )
    repository = models.OneToOneField(
        "github.GithubRepository",
        on_delete=models.CASCADE,
        related_name="app",
        null=True,
        blank=True,
    )

    app_type = models.ForeignKey(
        "AppType",
        on_delete=models.CASCADE,
        related_name="apps",
        blank=True,
        null=True,
    )
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    primary_language = models.ForeignKey(
        "github.GithubLanguage",
        on_delete=models.CASCADE,
        related_name="apps",
        blank=True,
        null=True,
    )

    links = GenericRelation(Link)

    status = models.CharField(max_length=16, choices=STATUS_OPTIONS, default="dev")

    class Meta:
        ordering = ["created_at"]

    def get_absolute_url(self):
        return reverse(view_names.APP, kwargs={"app_id": self.app_id})

    def all_text(self) -> str:
        return self.description

    def build_slug(self):
        return slugify(self.app_id.replace(".", "-"))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.build_slug()

        self.get_default_theme_from(self.app_type)

        if self.repository:
            self.primary_language = self.repository.primary_language
            self.description = self.repository.description

            super().save(*args, **kwargs)

            if self.repository.is_public():
                Link.objects.update_or_create(
                    url=self.repository.url,
                    content_type=ContentType.objects.get_for_model(self),
                    object_id=self.pk,
                    defaults={"description": "source"},
                )

        else:
            super().save(*args, **kwargs)

    def resolve_icon_url(self) -> Optional[str]:
        try:
            return self.icon.url
        except (AttributeError, ValueError):
            pass

    def resolve_icon_svg(self) -> Optional[str]:
        try:
            return self.app_type.icon_svg
        except (AttributeError, ValueError):
            pass

    @classmethod
    def resolve_from_url_kwargs(cls, app_id, **url_kwargs) -> "App":
        return cls.objects.get(app_id=app_id)

    def to_search_result(self) -> SearchResult:
        return SearchResult(
            name=self.title,
            description=self.description,
            timestamp=self.published_at,
            url=self.get_absolute_url(),
        )

    def __str__(self):
        return self.app_id
