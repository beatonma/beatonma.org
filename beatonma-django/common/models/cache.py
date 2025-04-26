from django.core.cache import cache
from django.db import models


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
        cache.delete_pattern(f"*{self.cache_key}*")
