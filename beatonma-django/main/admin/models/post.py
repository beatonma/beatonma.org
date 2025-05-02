from common.admin import BaseAdmin
from common.models.util import implementations_of
from django.contrib import admin
from main.admin.models.links import LinkInline
from main.admin.models.relatedfile import RelatedFileInline
from main.models import AppPost, ChangelogPost, Post
from main.models.rewrite import AboutPost
from main.models.rewrite.app import AppResource


@admin.action(description="save()")
def save_models(modeladmin, request, queryset):
    for obj in queryset:
        obj.save()


@admin.register(AboutPost)
class BasePostAdmin(BaseAdmin):
    actions = (save_models,)
    inlines = [
        LinkInline,
        RelatedFileInline,
    ]

    list_display = [
        "__str__",
        "slug",
        "is_published",
        "attachments",
        "published_at",
    ]

    editable_fields = (
        "slug",
        "allow_outgoing_webmentions",
        "is_published",
        "published_at",
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
        "tags",
    )

    field_order = (
        "is_published",
        "published_at",
        "slug",
        "color_muted",
        "color_vibrant",
        "title",
        "subtitle",
        "preview_text",
        "format",
        "content",
        "allow_outgoing_webmentions",
        "hero_image",
        "hero_embedded_url",
        "hero_html",
    )
    field_groups = (
        ("is_published", "published_at"),
        ("color_vibrant", "color_muted"),
        ("slug", "old_slug"),
        ("created_at", "modified_at"),
        ("id", "api_id"),
    )

    def attachments(self, obj):
        return obj.related_files.all().count()

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("related_files")

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ["content_script", "content", "content_html", "hero_html"]:
            kwargs["widget"] = self.widgets.textarea("font-mono!")
        return super().formfield_for_dbfield(db_field, **kwargs)


@admin.register(Post)
class PostAdmin(BasePostAdmin):
    def get_queryset(self, request):
        """We only want to show canonical Post instances, not those that are
        really a subclass (AppPost, ChangelogPost, ...)"""
        subclass_related_names = [
            x.__name__.lower() for x in implementations_of(Post) if x != Post
        ]

        exclude_subclasses = {
            f"{subclass}__isnull": True for subclass in subclass_related_names
        }

        return (
            super()
            .get_queryset(request)
            .filter(**exclude_subclasses)
            .prefetch_related("related_files")
        )


class AppResourceInline(admin.TabularInline):
    model = AppResource
    extra = 1


@admin.register(AppPost)
class AppPostAdmin(BasePostAdmin):
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
class ChangelogPostAdmin(BasePostAdmin):
    editable_fields = PostAdmin.editable_fields + (
        "app",
        "version",
    )
