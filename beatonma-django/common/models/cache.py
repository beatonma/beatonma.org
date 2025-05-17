import logging

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.db.models import QuerySet

log = logging.getLogger(__name__)


class InvalidateCacheQuerySet(QuerySet):
    def update(self, **kwargs):
        result = super().update(**kwargs)
        self.model.invalidate_cache()
        return result

    def delete(self):
        result = super().delete()
        self.model.invalidate_cache()
        return result


class InvalidateCacheMixin(models.Model):
    """Invalidate caches tagged with `cache_key` whenever the model is saved.

    Example usage:
        @decorate_view(cache_page(60 * 60, key_prefix=MyCachedModel.cache_key))
        def my_view...
    """

    class Meta:
        abstract = True

    queryset_class = InvalidateCacheQuerySet
    cache_key: str

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.invalidate_cache()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.invalidate_cache()

    @classmethod
    def invalidate_cache(cls):
        try:
            cache.delete_pattern(f"*{cls.cache_key}*")
        except AttributeError:
            if not settings.DEBUG:
                log.warning(f"Failed to invalidate cache '{cls.cache_key}'")
