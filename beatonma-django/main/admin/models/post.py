from common.admin import BaseAdmin
from django.contrib import admin
from main.admin.models.links import LinkInline
from main.admin.models.relatedfile import RelatedFileInline
from main.models import AppPost, ChangelogPost, Post
from main.models.rewrite import AboutPost
from main.models.rewrite.app import AppResource


@admin.register(Post, AboutPost)
class PostAdmin(BaseAdmin):
    inlines = [
        LinkInline,
        RelatedFileInline,
    ]

    list_display = [
        "title",
        "is_published",
        "published_at",
    ]

    editable_fields = (
        "allow_outgoing_webmentions",
        "is_published",
        "color_muted",
        "color_vibrant",
        "format",
        "hero_image",
        "hero_html",
        "hero_embedded_url",
        "title",
        "subtitle",
        "preview_text",
        "content",
        "content_script",
        "app",
    )

    field_order = (
        "allow_outgoing_webmentions",
        "is_published",
        "color_muted",
        "color_vibrant",
        "hero_image",
        "hero_embedded_url",
        "hero_html",
        "title",
        "subtitle",
        "preview_text",
        "format",
    )
    field_groups = (
        ("color_vibrant", "color_muted"),
        ("slug", "old_slug"),
        ("created_at", "modified_at", "published_at"),
        ("id", "api_id"),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ["content_script", "content", "content_html", "hero_html"]:
            kwargs["widget"] = self.widgets.textarea("font-mono!")
        return super().formfield_for_dbfield(db_field, **kwargs)


class AppResourceInline(admin.TabularInline):
    model = AppResource
    extra = 1


@admin.register(AppPost)
class AppPostAdmin(PostAdmin):
    inlines = PostAdmin.inlines + [AppResourceInline]

    editable_fields = PostAdmin.editable_fields + (
        "icon",
        "codename",
        "script",
        "script_html",
        "script_is_widget",
        "widget_style",
        "repository",
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "script":
            # Limit resource options to those associated with this AppPost
            qs = AppResource.objects.none()
            if request.resolver_match.kwargs:
                app_id = request.resolver_match.kwargs["object_id"]
                try:
                    app = AppPost.objects.get(pk=app_id)
                    qs = AppResource.objects.filter(app=app)
                except AppPost.DoesNotExist:
                    pass
            kwargs["queryset"] = qs

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ChangelogPost)
class ChangelogPostAdmin(PostAdmin):
    editable_fields = PostAdmin.editable_fields + (
        "app",
        "version",
    )
