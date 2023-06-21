from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """Provides created_at field with default ordering."""

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


from .api import ApiModel
from .pageview import PageView
from .published import PublishedMixin
from .search import SearchMixin
from .taggable import TaggableMixin
