from common.admin import BaseAdmin
from django.contrib import admin
from main.admin.models.links import LinkInline
from main.admin.models.relatedfile import RelatedFileInline
from main.models import Post


@admin.register(Post)
class PostAdmin(BaseAdmin):
    inlines = [
        LinkInline,
        RelatedFileInline,
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
    field_groups = [
        ["color_vibrant", "color_muted"],
        ["slug", "old_slug"],
        ["created_at", "modified_at", "published_at"],
        ["id", "api_id"],
    ]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ["content_script", "content", "content_html", "hero_html"]:
            kwargs["widget"] = self.widgets.textarea("font-mono!")
        return super().formfield_for_dbfield(db_field, **kwargs)
