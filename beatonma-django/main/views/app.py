import logging

from common.views.logged import LoggedView
from common.views.mentionable import MentionableView
from django.shortcuts import get_object_or_404, render
from main.models import App

from .util.color import get_theme_context

log = logging.getLogger(__name__)


class AppView(MentionableView, LoggedView):
    def get(self, request, app_id: str):
        app = get_object_or_404(
            App.objects.prefetch_related(
                "changelogs",
                "related_files",
                "tags",
            ),
            app_id=app_id,
        )
        changelogs = app.changelogs.published().prefetch_related(
            "links",
            "related_files",
            "tags",
        )

        return render(
            request,
            "pages/posts/app/app.html",
            {
                "post": app,
                "changelogs": changelogs,
                **get_theme_context(app),
            },
        )
