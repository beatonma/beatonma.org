import uuid

from common.models import BaseModel
from django.contrib.auth.models import User
from django.db import models


class ApiToken(BaseModel):
    enabled = models.BooleanField(default=False)
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)

    user = models.ForeignKey(
        User,
        editable=False,
        on_delete=models.CASCADE,
        related_name="api_tokens",
        related_query_name="api_token",
    )

    def __str__(self):
        enabled = "✓" if self.enabled else "✕"
        return f"{enabled} {self.user}: {self.uuid}"
