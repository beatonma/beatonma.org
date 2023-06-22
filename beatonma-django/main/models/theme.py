from common.models import BaseModel
from django.db import models
from main.models.mixins import ThemeableMixin
from main.models.mixins.ephemeral import EphemeralMixin


class ThemeOverride(EphemeralMixin, ThemeableMixin, BaseModel):
    search_enabled = False

    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        ordering = [
            "-is_published",
            "public_from",
            "public_until",
            "-created_at",
        ]
