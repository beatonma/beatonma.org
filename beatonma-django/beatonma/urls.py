"""beatonma URL Configuration."""

from bma_app.api import api as bma_app_api
from contact.api import router as contact_router
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from github.api import router as github_router
from main.api import public_api
from webmentions_tester.api import router as webmentions_tester_router


def _redirect(url: str):
    return RedirectView.as_view(url=url, permanent=True)


redirects = [
    path("github/", _redirect("https://github.com/beatonma")),
    path("music/", _redirect("https://www.last.fm/user/schadenfreude87")),
    path("youtube/", _redirect("https://www.youtube.com/@fallofmath")),
]


local_urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path(settings.BMA_NOTIFICATIONS_URL, include("bmanotify_django.urls")),
]

public_api.add_router("contact/", contact_router)
public_api.add_router("webmentions_tester/", webmentions_tester_router)
public_api.add_router("github/", github_router)

urlpatterns = (
    [
        path("api/", public_api.urls),
        path("api/webmention/", include("mentions.urls")),
        path("api/v2/", bma_app_api.urls),
        path("", include("main.urls")),
    ]
    + redirects
    + local_urlpatterns
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + debug_toolbar_urls()
)
