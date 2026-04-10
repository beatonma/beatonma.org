from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from common.models import BaseModel


class CachedResponse(BaseModel):
    """Stores pre-constructed data for github-events/ endpoint."""

    data = models.JSONField(encoder=DjangoJSONEncoder)

    def __str__(self):
        return f"{self.created_at}"
