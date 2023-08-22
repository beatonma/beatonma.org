import logging

from bma_dev.models import DevThemePreview
from common.views.logged import LoggedView
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseGone,
)
from django.shortcuts import render
from main.models import AppType
from main.views.util import get_theme_context

log = logging.getLogger(__name__)


class DevThemeView(LoggedView):
    reverse_name = "dev_theme_preview"

    def get(self, request):
        return render(
            request,
            "pages/debug/theme-preview.html",
            {
                "app_types": AppType.objects.all(),
                **get_theme_context(DevThemePreview.objects.first()),
            },
        )


class SimulatedErrorView(LoggedView):
    reverse_name = "dev_simulated_error"

    def get(self, request, error_code: int):
        if 400 <= error_code < 500:
            log.warning(f"SimulatedErrorView[{error_code}]: Nothing to worry about.")

        if error_code == 400:
            return HttpResponseBadRequest()
        elif error_code == 403:
            return HttpResponseForbidden()
        elif error_code == 404:
            raise Http404()
        elif error_code == 410:
            return HttpResponseGone()
        elif error_code < 500:
            return HttpResponse(status=error_code)

        raise Exception(f"SimulatedErrorView[{error_code}]: Nothing to worry about.")
