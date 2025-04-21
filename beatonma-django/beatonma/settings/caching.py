from beatonma.settings import environment

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": environment.CACHE_LOCATION,
    }
}
