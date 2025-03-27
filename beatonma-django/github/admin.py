from common.admin import BaseAdmin, register_models_to_default_admin
from django.contrib import admin
from github.models import GithubRepository


@admin.action(description="Make private")
def _action_make_private(modeladmin, request, queryset):
    queryset.update(is_published=False)


@admin.action(description="Make public")
def _action_make_public(modeladmin, request, queryset):
    queryset.update(is_published=True)


class GithubAdmin(BaseAdmin):
    editable_fields = [
        "is_published",
    ]


@admin.register(GithubRepository)
class RepoAdmin(GithubAdmin):
    search_fields = [
        "name",
    ]
    list_display = [
        "name",
        "is_published",
        "_size",
        "license",
        "published_at",
    ]
    ordering = [
        "-published_at",
    ]

    actions = [
        _action_make_public,
        _action_make_private,
    ]

    def _size(self, obj: GithubRepository) -> str:
        return f"{obj.size_kb}kb"
