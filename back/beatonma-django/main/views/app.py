import logging

from common.views.logged import LoggedView
from common.views.mentionable import MentionableView
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from main.models import App, Changelog

from .util.color import get_theme_context

log = logging.getLogger(__name__)


class AppView(MentionableView, LoggedView):
    def get(self, request, app_id: str):
        try:
            app = App.objects.get(app_id=app_id)
        except ObjectDoesNotExist:
            raise Http404()

        changelogs = Changelog.objects.filter(app=app)

        return render(
            request,
            "pages/posts/app/app.html",
            {
                "app": app,
                "changelogs": changelogs,
                **get_theme_context(app),
            },
        )
