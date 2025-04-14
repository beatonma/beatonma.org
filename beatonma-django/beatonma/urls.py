"""beatonma URL Configuration."""

from typing import Any

from bma_app.api import api as bma_app_api
from contact.api import router as contact_router
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import include, path
from django.views.generic import RedirectView
from github.api import router as github_router
from main.api import public_api


def _redirect(url: str):
    return RedirectView.as_view(url=url, permanent=True)


def _root_template(name: Any):
    return lambda request, *args, **kwargs: TemplateResponse(request, f"{name}.html")


local_urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path(settings.DASHBOARD_URL, include("dashboard.urls")),
    path(settings.BMA_NOTIFICATIONS_URL, include("bmanotify_django.urls")),
]

redirects = [
    path(
        "github/",
        _redirect("https://github.com/beatonma"),
    ),
    path(
        "music/",
        _redirect(
            "https://www.last.fm/user/schadenfreude87",
        ),
    ),
    path(
        "youtube/",
        _redirect("https://www.youtube.com/@fallofmath"),
    ),
]


errors = [
    path("400/", _root_template(400)),
    path("403/", _root_template(403)),
    path("404/", _root_template(404)),
    path("500/", _root_template(500)),
]

public_api.add_router("contact/", contact_router)

urlpatterns = (
    [
        path("api/", public_api.urls),
        path("api/webmention/", include("mentions.urls")),
        path("webmentions_tester/", include("webmentions_tester.urls")),
        path("api/v2/", bma_app_api.urls),
        # path("wurdle/", include("webapp.wurdle.urls")),
        path("", include("main.urls")),
        path("", include("bma_dev.urls")),
    ]
    + redirects
    + errors
    + local_urlpatterns
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + debug_toolbar_urls()
)
