import logging

from common.models import BaseModel
from django.db import models
from main.models.mixins.ephemeral import EphemeralMixin

log = logging.getLogger(__name__)


class MessageOfTheDay(EphemeralMixin, BaseModel):
    search_enabled = False

    title = models.CharField(max_length=64, blank=True, null=True)
    content = models.TextField()

    def __str__(self):
        return self.title or f"{self.content[:30].strip()}..."

    class Meta:
        verbose_name_plural = "Messages of the Day"
