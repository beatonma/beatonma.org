"""beatonma URL Configuration."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

local_urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path(settings.DASHBOARD_URL, include("dashboard.urls")),
    path(settings.BMA_NOTIFICATIONS_URL, include("bmanotify_django.urls")),
]

redirects = [
    path(
        "github/",
        RedirectView.as_view(url="https://github.com/beatonma", permanent=True),
    ),
    path(
        "music/",
        RedirectView.as_view(
            url="https://www.last.fm/user/schadenfreude87",
            permanent=True,
        ),
    ),
    path(
        "playstore/",
        RedirectView.as_view(
            url="https://play.google.com/store/apps/developer?id=Michael+Beaton",
            permanent=True,
        ),
    ),
    path(
        "starcraft/",
        RedirectView.as_view(
            url="https://starcraft2.com/en-gb/profile/2/1/2784180",
            permanent=True,
        ),
    ),
]

urlpatterns = (
    local_urlpatterns
    + redirects
    + [
        path("", include("main.urls")),
        path("api/", include("bma_app.urls")),
        path("webmention/", include("mentions.urls")),
        path("contact/", include("contact.urls")),
        path("webmentions_tester/", include("webmentions_tester.urls")),
        path("wurdle/", include("webapp.wurdle.urls")),
        path("", include("bma_dev.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
