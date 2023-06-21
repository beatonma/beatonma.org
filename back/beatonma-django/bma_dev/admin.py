from bma_dev.models import DevThemePreview
from common.admin import BaseAdmin
from django.contrib import admin
from django.utils.safestring import mark_safe


@admin.register(DevThemePreview)
class ThemePreviewAdmin(BaseAdmin):
    list_display = [
        "__str__",
        "_color_muted",
        "_color_vibrant",
    ]

    def _color_preview(self, color):
        return mark_safe(
            '<div style="'
            "padding:4px 8px;"
            "border-radius:4px;"
            "color:white;"
            f"background-color:{color};"
            f'">{color}</div>'
        )

    def _color_muted(self, obj):
        return self._color_preview(obj.color_muted)

    def _color_vibrant(self, obj):
        return self._color_preview(obj.color_vibrant)
