from django.core.cache.backends.dummy import DummyCache


class DummyRedisCache(DummyCache):
    def delete_pattern(self, glob: str):
        return
