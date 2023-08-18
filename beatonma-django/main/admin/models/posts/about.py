from common.admin import BaseAdmin
from django.contrib import admin
from main.models.posts import About


@admin.register(About)
class AboutAdmin(BaseAdmin):
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
