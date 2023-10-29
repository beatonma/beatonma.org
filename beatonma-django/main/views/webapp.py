import logging
from typing import Optional

from common.views.logged import LoggedView
from django.contrib.staticfiles import finders
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.templatetags.static import StaticNode
from main.models import WebApp

log = logging.getLogger(__name__)


class WebAppView(LoggedView):
    def get(self, request, slug: str):
        response = _serve_uploaded_webapp(request, slug) or _serve_static_webapp(
            request, slug
        )
        if response:
            return response
        raise Http404


def _serve_uploaded_webapp(request, slug: str) -> Optional[HttpResponse]:
    webapp = WebApp.objects.filter(slug=slug).first()
    if webapp:
        return render(
            request,
            "pages/webapp.html",
            {
                "webapp": webapp,
            },
        )


def _serve_static_webapp(request, slug: str) -> Optional[HttpResponse]:
    filename = f"webapp/{slug}.js"
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

    log.warning(f"Unknown webapp: {filename}")
