from common.models import BaseModel
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models


class CachedResponse(BaseModel):
    """Stores pre-constructed data for github-events/ endpoint."""

    data = models.JSONField(encoder=DjangoJSONEncoder)

    def __str__(self):
        return f"{self.created_at}"
