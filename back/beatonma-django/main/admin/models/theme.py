from common.admin import BaseAdmin
from django.contrib import admin
from django.utils import timezone
from django.utils.safestring import mark_safe
from main.admin.icons import admin_icon_check, admin_icon_cross
from main.models import ThemeOverride


@admin.register(ThemeOverride)
class ThemeOverrideAdmin(BaseAdmin):
    list_display = [
        "__str__",
        "_color_muted",
        "_color_vibrant",
        "_is_active",
        "is_published",
        "_public_from",
        "_public_until",
    ]

    fields = [
        "is_published",
        "name",
        "color_muted",
        "color_vibrant",
        "public_from",
        "public_until",
        "published_at",
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

    def _public_from(self, obj):
        now = timezone.now()
        if obj.public_from is None or obj.public_from <= now:
            icon = admin_icon_check()
        else:
            icon = admin_icon_cross()

        return mark_safe(f"{icon} {obj.public_from}")

    def _public_until(self, obj):
        now = timezone.now()
        if obj.public_until is None or obj.public_until > now:
            icon = admin_icon_check()
        else:
            icon = admin_icon_cross()

        return mark_safe(f"{icon} {obj.public_until}")

    def _is_active(self, obj):
        if obj.is_active():
            return admin_icon_check()
        return admin_icon_cross()
