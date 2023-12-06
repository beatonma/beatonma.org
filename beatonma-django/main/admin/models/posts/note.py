from django.contrib import admin
from main.admin.models.posts import actions, fieldsets
from main.admin.models.posts.webpost import WebPostAdmin
from main.models import Note


@admin.register(Note)
class NoteAdmin(WebPostAdmin):
    actions = actions.PUBLISH_ACTIONS
    list_display = [
        "_content",
        "_files",
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
        fieldsets.METADATA,
        fieldsets.generated_html("content_html"),
    )

    def _files(self, obj: Note) -> str:
        return obj.related_files.all().count()

    def _content(self, obj: Note) -> str:
        return obj.content or "-"
