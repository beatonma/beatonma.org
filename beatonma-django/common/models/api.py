import uuid

from django.db import models


class ApiEditable(models.Model):
    """ID to be used in any potentially public contexts."""

    api_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
