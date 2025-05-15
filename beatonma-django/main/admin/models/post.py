from common.admin import BaseAdmin
from common.models.util import implementations_of
from django.contrib import admin
from django.utils.safestring import mark_safe
from main.admin.models import inline
from main.admin.util import pluralize
from main.models import AboutPost, AppPost, ChangelogPost, Feed, Post
from main.models.formats import Formats
from main.models.posts.app import AppResource


@admin.action
def publish(modeladmin, request, queryset):
    queryset.update(is_published=True)


@admin.action
def unpublish(modeladmin, request, queryset):
    queryset.update(is_published=False)


@admin.action
def save(modeladmin, request, queryset):
    for item in queryset.all():
        item.save()


class BasePostAdmin(BaseAdmin):
    actions = [
        publish,
        unpublish,
        save,
    ]

    inlines = [
        inline.LinkInline,
        inline.RelatedFileInline,
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
        "preview",
        "content",
        "content_script",
        "tags",
        "feeds",
    )

    field_order = (
        "is_published",
        "published_at",
        "slug",
        "color_muted",
        "color_vibrant",
        "title",
        "subtitle",
        "preview",
        "format",
        "content",
        "feeds",
        "allow_outgoing_webmentions",
        "hero_image",
        "hero_embedded_url",
        "hero_html",
    )
    field_groups = (
        ("published_at", "is_published", "allow_outgoing_webmentions"),
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


@admin.register(AboutPost)
class AboutPostAdmin(BasePostAdmin):
    pass


@admin.register(Post)
class PostAdmin(BasePostAdmin):
    def get_queryset(self, request):
        return (
            super().get_queryset(request).posts_only().prefetch_related("related_files")
        )


@admin.register(AppPost)
class AppPostAdmin(BasePostAdmin):
    inlines = PostAdmin.inlines + [inline.AppResourceInline]

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


@admin.register(Feed)
class FeedAdmin(BaseAdmin):
    editable_fields = [
        "is_published",
        "published_at",
        "slug",
        "name",
    ]

    @admin.display(description="Posts")
    def _field_posts(self, obj):
        posts = obj.posts.all()
        n = posts.count()

        if n == 0:
            return "No posts"

        markdown = (
            "**"
            + pluralize(n, "{} post", "{} posts")
            + "**"
            + "\n"
            + ("\n".join([f"- {str(x).replace("\n", "")}" for x in posts]))
        )
        return mark_safe(Formats.to_html(markdown, basic=True))
