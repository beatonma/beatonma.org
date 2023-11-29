import uuid

from django.db import models


class ApiModel:
    def to_json(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement to_json()"
        )


class ApiEditable(models.Model):
    """ID to be used in any potentially public contexts."""

    api_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
