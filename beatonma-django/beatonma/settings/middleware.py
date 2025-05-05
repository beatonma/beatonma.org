from . import environment

_DJANGO_MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
]
_THIRD_PARTY_MIDDLEWARE = [
    "django_user_agents.middleware.UserAgentMiddleware",
]
_PROJECT_MIDDLEWARE = [
    "mentions.middleware.WebmentionHeadMiddleware",
]
_DEBUG_MIDDLEWARE = [
    "bma_dev.middleware.cors_middleware",
]
MIDDLEWARE = _DJANGO_MIDDLEWARE + _THIRD_PARTY_MIDDLEWARE + _PROJECT_MIDDLEWARE
if environment.DEBUG and not environment.TESTING:
    MIDDLEWARE.insert(
        MIDDLEWARE.index(
            "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware"
        ),
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    )
    MIDDLEWARE += _DEBUG_MIDDLEWARE
