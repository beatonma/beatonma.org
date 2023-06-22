from django.contrib import admin

from common.admin import BaseAdmin
from main.models.posts import About


@admin.register(About)
class AboutAdmin(BaseAdmin):
    admin_app_priority = 1
    admin_priority = 1

    list_display = [
        "description",
        "created_at",
        "active",
    ]

    readonly_fields = [
        "content_html",
    ]

    date_hierarchy = "created_at"
    ordering = ["-active", "-created_at"]
