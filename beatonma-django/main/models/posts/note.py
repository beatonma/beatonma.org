import uuid

from common.models import ApiModel
from django.db import models
from django.urls import reverse
from main.models.posts.formats import Formats
from main.models.posts.webpost import BasePost
from main.util import to_absolute_url
from main.views import view_names


class Note(ApiModel, BasePost):
    max_length: int = 280
    search_fields = ["content", "tags__name"]

    content = models.CharField(max_length=max_length, default="", blank=True)
    slug = models.SlugField(unique=True, max_length=7, editable=False)

    def is_publishable(self) -> bool:
        # Don't show notes that have neither text content nor media.
        return (
            not (self.content.strip() == "" and self.related_files.all().count() == 0)
        ) and super().is_publishable()

    def build_slug(self):
        return uuid.uuid4().hex[:7]

    def get_absolute_url(self):
        return reverse(view_names.NOTE, kwargs={"slug": self.slug})

    def all_text(self):
        return self.content_html

    def save_text(self):
        self.content_html = Formats.to_html(Formats.MARKDOWN, self.content)

    def to_json(self) -> dict:
        return {
            "content": self.content_html,
            "url": to_absolute_url(self.get_absolute_url()),
            "timestamp": self.published_at,
            "is_published": self.is_published,
        }
