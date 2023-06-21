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
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        fields = [x.name for x in self.get_model_fields(model)]
        self.readonly_fields = [x for x in fields if x != "is_published"]


@admin.register(GithubRepository)
class RepoAdmin(GithubAdmin):
    list_display = [
        "name",
        "is_published",
        "_size",
        "license",
    ]

    actions = [
        _action_make_public,
        _action_make_private,
    ]

    def _size(self, obj: GithubRepository) -> str:
        return f"{obj.size_kb}kb"


register_models_to_default_admin("github", GithubAdmin)
