import logging

from common.models import BaseModel
from django.db import models
from main.models.mixins.cache import GlobalStateCacheMixin
from main.models.mixins.ephemeral import EphemeralMixin

log = logging.getLogger(__name__)


class MessageOfTheDay(GlobalStateCacheMixin, EphemeralMixin, BaseModel):
    search_enabled = False

    description = models.CharField(
        max_length=64, blank=True, null=True, help_text="Admin only"
    )
    content_html = models.TextField()

    def __str__(self):
        return self.description or f"{self.content_html[:64].strip()}..."

    class Meta:
        verbose_name_plural = "Messages of the Day"
