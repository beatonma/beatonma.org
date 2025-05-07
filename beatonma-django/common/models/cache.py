import logging

from django.conf import settings
from django.core.cache import cache
from django.db import models

log = logging.getLogger(__name__)


class InvalidateCacheMixin(models.Model):
    """Invalidate caches tagged with `cache_key` whenever the model is saved.

    Example usage:
        @decorate_view(cache_page(60 * 60, key_prefix=MyCachedModel.cache_key))
        def my_view...
    """

    class Meta:
        abstract = True

    cache_key: str

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            cache.delete_pattern(f"*{self.cache_key}*")
        except AttributeError:
            if not settings.DEBUG:
                log.warning(f"Failed to invalidate cache '{self.cache_key}'")
