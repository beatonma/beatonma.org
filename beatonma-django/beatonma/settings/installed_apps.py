from . import environment

_DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.flatpages",
    "django.contrib.messages",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
]
_THIRD_PARTY_APPS = [
    "adminsortable2",
    "colorfield",
    "taggit",
    "django_extensions",
    "django_user_agents",
]
_FIRST_PARTY_APPS = [
    "bmanotify_django",
    "mentions",
]
_PROJECT_APPS = [
    "bma_app",
    "bma_dev",
    "common",
    "contact",
    "github",
    "main",
    "webmentions_tester",
]
_DEBUG_APPS = [
    "debug_toolbar",
]
INSTALLED_APPS = _DJANGO_APPS + _THIRD_PARTY_APPS + _FIRST_PARTY_APPS + _PROJECT_APPS
if environment.DEBUG and not environment.TESTING:
    INSTALLED_APPS += _DEBUG_APPS
