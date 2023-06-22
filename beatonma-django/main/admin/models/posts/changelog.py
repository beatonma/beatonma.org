from django.contrib import admin
from main.admin.models.posts import fieldsets
from main.admin.models.posts.webpost import WebPostAdmin
from main.models import Changelog


@admin.register(Changelog)
class ChangelogAdmin(WebPostAdmin):
    list_display = [
        "app",
        "version_name",
        "published_at",
        "tagline",
    ]

    fieldsets = (
        (
            "Changelog",
            {
                "fields": (
                    "app",
                    "version_name",
                    "title",
                    "tagline",
                    "preview_text",
                    "format",
                    "content",
                    "tags",
                ),
            },
        ),
        fieldsets.PUBLISHING,
        fieldsets.METADATA,
        fieldsets.generated_html("content_html"),
    )
