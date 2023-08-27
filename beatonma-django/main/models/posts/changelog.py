from common.models.search import SearchResult
from django.db import models
from django.utils.text import slugify
from main.models import App
from main.models.posts.webpost import RichWebPost


class Changelog(RichWebPost):
    """A list of changes included in an app update."""

    title = models.CharField(max_length=255, blank=True)
    app = models.ForeignKey(
        App,
        null=True,
        on_delete=models.CASCADE,
        related_name="changelogs",
    )
    version_name = models.CharField(max_length=30, help_text="")

    class Meta:
        ordering = ["-published_at"]

    def preview_title(self):
        return f"Changelog: {self.app.title} {self.version_name}"

    def get_absolute_url(self):
        return f"{self.app.get_absolute_url()}#{self.version_name}"

    def build_slug(self):
        return slugify(f"{self.app.app_id}-{self.version_name}".replace(".", "-"))

    def save_text(self):
        if self.title == "":
            self.title = self.version_name

        super().save_text()

    def to_search_result(self) -> SearchResult:
        return SearchResult(
            name=f"{self.app.title}: {self.version_name}",
            description=self.preview_text,
            timestamp=self.published_at,
            url=self.get_absolute_url(),
        )

    def __str__(self):
        return f"{self.app} {self.version_name}"
