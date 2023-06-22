from django.contrib import admin
from main.admin.models.posts import actions, fieldsets
from main.admin.models.posts.webpost import WebPostAdmin
from main.models import Note


@admin.register(Note)
class NoteAdmin(WebPostAdmin):
    readonly_fields = [
        "content_html",
        "created_at",
        "slug",
    ]
    actions = actions.PUBLISH_ACTIONS
    list_display = [
        "content",
        "is_published",
    ]
    list_filter = [
        "is_published",
        "created_at",
    ]
    search_fields = [
        "content",
        "tags",
    ]
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Note",
            {
                "fields": (
                    "content",
                    "tags",
                ),
            },
        ),
        fieldsets.PUBLISHING,
        (
            "Metadata",
            {
                "classes": ("collapse",),
                "fields": (
                    "slug",
                    "created_at",
                ),
            },
        ),
        fieldsets.generated_html("content_html"),
    )
