from common.admin import BaseAdmin
from django.contrib import admin
from main.admin.models.links import LinkInline
from main.admin.models.posts.actions import PUBLISH_ACTIONS
from main.admin.models.relatedfile import RelatedFileInline
from main.models import App, AppType, Host, Link


@admin.register(App)
class AppAdmin(BaseAdmin):
    list_display = ["title", "app_id", "app_type", "is_published"]
    prepopulated_fields = {
        "slug": ("app_id",),
    }
    inlines = [
        RelatedFileInline,
        LinkInline,
    ]
    actions = PUBLISH_ACTIONS

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if form.instance.repository:
            # Copy tags from repository if available.
            form.instance.tags.add(*form.instance.repository.tags.all())


@admin.register(AppType)
class AppTypeAdmin(BaseAdmin):
    list_display = [
        "name",
    ]


@admin.register(Host)
class HostAdmin(BaseAdmin):
    list_display = [
        "name",
        "domain",
    ]


@admin.register(Link)
class LinkAdmin(BaseAdmin):
    list_display = [
        "url",
        "description",
        "host",
    ]
