from bma_dev.models import DevThemePreview
from common.views.logged import LoggedView
from django.shortcuts import render
from main.models import AppType
from main.views.util import get_theme_context


class DevThemeView(LoggedView):
    reverse_name = "dev_theme_preview"

    def get(self, request):
        return render(
            request,
            "pages/debug/theme-preview.html",
            dict(
                app_types=AppType.objects.all(),
                **get_theme_context(DevThemePreview.objects.first()),
            ),
        )
