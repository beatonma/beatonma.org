from common.models.cache import InvalidateCacheMixin


class GlobalStateCacheMixin(InvalidateCacheMixin):
    cache_key = "__global_state__"

    class Meta:
        abstract = True
