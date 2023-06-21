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
    "main.middleware.redirect.QueryableRedirectFallbackMiddleware",
]
MIDDLEWARE = _DJANGO_MIDDLEWARE + _THIRD_PARTY_MIDDLEWARE + _PROJECT_MIDDLEWARE
