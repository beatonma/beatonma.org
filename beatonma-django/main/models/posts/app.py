import logging
from typing import Optional

from common.models import BaseModel
from common.models.search import SearchResult
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from main.forms import SanitizedFileField
from main.models.formats import FormatMixin, Formats
from main.models.link import Link
from main.models.mixins.styleable_svg import StyleableSvgMixin
from main.models.mixins.themeable import ThemeableMixin
from main.models.posts.webpost import BasePost
from main.view_adapters import FeedItemContext
from main.views import view_names

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
    BasePost,
    FormatMixin,
    ThemeableMixin,
    BaseModel,
):
    class StatusOptions(models.TextChoices):
        dev = "dev"
        test = "test"
        public = "published"
        deprecated = "deprecated"

    search_fields = ["title", "content", "app_id", "tags__name"]

    title = models.CharField(max_length=140)
    app_id = models.CharField(max_length=255, unique=True, help_text="Application ID")
    slug = models.SlugField(unique=True, max_length=255)
    tagline = models.CharField(max_length=140, blank=True)
    status = models.CharField(
        max_length=16,
        choices=StatusOptions.choices,
        default="dev",
        blank=True,
        null=True,
    )

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

    class Meta:
        ordering = ["created_at"]

    def get_absolute_url(self):
        return reverse(view_names.APP, kwargs={"app_id": self.app_id})

    def get_content_html(self) -> str:
        return self.content_html

    def save_text(self):
        self.content_html = Formats.to_html(self.format, self.content)

    def build_slug(self):
        return slugify(self.app_id.replace(".", "-"))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.build_slug()

        self.get_default_theme_from(self.app_type)

        if self.repository:
            self._update_from_repository(*args, **kwargs)

        else:
            super().save(*args, **kwargs)

    def _update_from_repository(self, *save_args, **save_kwargs):
        self.primary_language = self.repository.primary_language
        super().save(*save_args, **save_kwargs)

        content_type = ContentType.objects.get_for_model(self)
        if self.repository.is_public():
            Link.objects.update_or_create(
                url=self.repository.url,
                content_type=content_type,
                object_id=self.pk,
                defaults={"description": "source"},
            )
        else:
            Link.objects.filter(
                url=self.repository.url,
                content_type=content_type,
                object_id=self.pk,
            ).delete()

    def resolve_icon_url(self) -> str | None:
        try:
            return self.icon.url
        except (AttributeError, ValueError):
            pass

    def resolve_icon_svg(self) -> str | None:
        try:
            return self.app_type.icon_svg
        except (AttributeError, ValueError):
            pass

    @classmethod
    def resolve_from_url_kwargs(cls, app_id, **url_kwargs) -> "App":
        return cls.objects.get(app_id=app_id)

    def resolve_description(self) -> str | None:
        if self.content_html:
            return self.content_html

        if self.repository:
            return self.repository.description

    def resolve_short_description(self) -> str | None:
        if self.tagline:
            return self.tagline

        if self.repository:
            return self.repository.description

    def to_search_result(self) -> SearchResult:
        return SearchResult(
            name=self.title,
            description=self.resolve_short_description(),
            timestamp=self.published_at,
            url=self.get_absolute_url(),
        )

    def to_feeditem_context(self) -> FeedItemContext:
        return FeedItemContext(
            title=self.title,
            url=self.get_absolute_url(),
            date=self.published_at,
            type=self.__class__.__name__,
            summary=self.resolve_short_description(),
            image_class="contain",
            image_url=self.resolve_icon_url(),
            themeable=self,
        )

    def __str__(self):
        return self.app_id
