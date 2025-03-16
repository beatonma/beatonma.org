from django.http import HttpRequest
from github.events import GithubEvent

from . import environment

# celery
CELERY_BROKER_URL = environment.CELERY_BROKER_URL


# django-debug-toolbar
def _should_show_debug_toolbar(request: HttpRequest) -> bool:
    from django.conf import settings

    return settings.DEBUG and not settings.TESTING


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": _should_show_debug_toolbar,
}


# django-ninja
NINJA_PAGINATION_PER_PAGE = 24
NINJA_PAGINATION_CLASS = "main.api.pagination.LimitOffsetPagination"


# notify
FCM_PROJECT_ID = environment.FCM_PROJECT_ID
FCM_SERVICE_ACCOUNT_FILE = environment.FCM_SERVICE_ACCOUNT_FILE

# github
GITHUB_ACCESS_TOKEN = environment.GITHUB_ACCESS_TOKEN
GITHUB_USERNAME = environment.GITHUB_USERNAME
GITHUB_EVENTS = [
    GithubEvent.CreateEvent,
    GithubEvent.IssuesEvent,
    GithubEvent.PullRequestEvent,
    GithubEvent.PushEvent,
    GithubEvent.ReleaseEvent,
    GithubEvent.WikiEvent,
]

# mentions
WEBMENTIONS_AUTO_APPROVE = True

# sentry
if environment.SENTRY_ENABLED:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=environment.SENTRY_DSN,
        integrations=[DjangoIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=0.6,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=False,
    )

# taggit
TAGGIT_CASE_INSENSITIVE = True

# webmentions_tester
TEMPORARY_WEBMENTION_TIME_TO_LIVE = 60 * 10
