import logging
import os
from pathlib import Path

from common.views.logged import LoggedView
from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import Http404
from django.shortcuts import render
from django.templatetags.static import StaticNode
from main.models import WebApp

log = logging.getLogger(__name__)


class WebAppView(LoggedView):
    def get(self, request, slug: str):
        webapp = WebApp.objects.filter(slug=slug).first()
        if webapp:
            return render(
                request,
                "pages/webapp.html",
                {
                    "webapp": webapp,
                },
            )

        if os.path.exists(Path(settings.BASE_DIR) / f"webapp/static/{slug}/"):
            filename = f"{slug}/js/{slug}-{settings.GIT_HASH}.min.js"
            app_script = finders.find(filename)

            if app_script:
                script_url = StaticNode.handle_simple(filename)
                log.info(f"Serving webapp: '{script_url}'")
                return render(
                    request,
                    "pages/webapp-react.html",
                    {
                        "react_app": {
                            "name": slug,
                            "url": script_url,
                        },
                    },
                )

            else:
                log.warning(f"Unknown webapp: {filename}")

        raise Http404()
