import math

from common.models import ApiModel, BaseModel, PublishedMixin, TaggableMixin
from common.models.search import SearchResult
from django.db import models
from django.db.models import UniqueConstraint


class GithubLanguage(BaseModel):
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="e.g. Java, Python, CSS...",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class GithubUser(BaseModel):
    id = models.PositiveIntegerField(unique=True, primary_key=True, editable=False)
    username = models.CharField(max_length=64, editable=False)
    url = models.URLField(editable=False)
    avatar_url = models.URLField(editable=False)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["username"]


class GithubLicense(BaseModel):
    key = models.CharField(max_length=64, editable=False, unique=True)
    name = models.CharField(max_length=64, editable=False)
    url = models.URLField(editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class GithubRepository(PublishedMixin, ApiModel, TaggableMixin, BaseModel):
    search_fields = ["name", "description"]

    id = models.PositiveIntegerField(unique=True, primary_key=True, editable=False)
    url = models.URLField(editable=False)
    updated_at = models.DateTimeField(editable=False)

    owner = models.ForeignKey(
        "GithubUser",
        on_delete=models.CASCADE,
        related_name="repositories",
        editable=False,
    )

    name = models.CharField(max_length=256, editable=False)
    full_name = models.CharField(max_length=256, editable=False)
    description = models.TextField(null=True, editable=False)

    # Represents the privacy status of this repository on Github.
    # This is separate from and not necessarily opposite to `is_published` field from PublishedMixin.
    is_private = models.BooleanField(editable=False)
    size_kb = models.PositiveIntegerField(editable=False)
    primary_language = models.ForeignKey(
        GithubLanguage,
        on_delete=models.CASCADE,
        null=True,
        editable=False,
    )

    license = models.ForeignKey(
        GithubLicense,
        on_delete=models.CASCADE,
        related_name="repositories",
        null=True,
        blank=True,
        editable=False,
    )

    def get_absolute_url(self):
        return self.url

    def is_public(self) -> bool:
        return self.is_published and not self.is_private

    def to_json(self):
        if not self.is_published:
            return None

        if self.is_private:
            return dict(
                name=self.name,
            )

        else:
            return dict(
                id=self.id,
                name=self.full_name,
                url=self.url,
                description=self.description,
                license=self.license.key if self.license else None,
            )

    def to_search_result(self) -> SearchResult:
        return SearchResult(
            name=self.full_name,
            description=self.description,
            timestamp=self.published_at,
            url=self.url,
        )

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ["-updated_at"]
        verbose_name_plural = "Github Repositoriies"


class GithubLanguageUsage(ApiModel, BaseModel):
    repository = models.ForeignKey(
        GithubRepository,
        on_delete=models.CASCADE,
        related_name="languages",
    )
    language = models.ForeignKey(
        GithubLanguage,
        on_delete=models.CASCADE,
        related_name="+",
    )
    size_bytes = models.PositiveIntegerField()

    @property
    def size_kb(self) -> int:
        return math.ceil(self.size_bytes / 1024.0)

    def to_json(self) -> dict:
        return dict(
            name=self.language.name,
            bytes=self.size_bytes,
        )

    def __str__(self):
        return f"{self.repository} | {self.language} {self.size_kb}kb"

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["repository", "language"],
                name="unique_language_per_repository",
            ),
        ]
        ordering = [
            "repository",
            "size_bytes",
        ]
