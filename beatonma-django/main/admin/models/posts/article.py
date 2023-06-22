from django.contrib import admin

from main.admin.models.posts import fieldsets
from main.admin.models.posts.webpost import WebPostAdmin
from main.models import Article


@admin.register(Article)
class ArticleAdmin(WebPostAdmin):
    readonly_fields = WebPostAdmin.readonly_fields + [
        "abstract_html",
    ]

    fieldsets = (
        (
            "Article",
            {
                "fields": (
                    "title",
                    "tagline",
                    "preview_text",
                    "format",
                    "abstract",
                    "content",
                    "tags",
                    "apps",
                ),
            },
        ),
        (
            "Advanced",
            {
                "classes": ("collapse",),
                "fields": (
                    "hero_html",
                    "content_script",
                ),
            },
        ),
        fieldsets.PUBLISHING,
        fieldsets.THEME,
        (
            "Styling",
            {
                "fields": (
                    (
                        "preview_image",
                        "preview_image_css",
                    ),
                    (
                        "hero_image",
                        "hero_css",
                        "hero_banner_css",
                    ),
                )
            },
        ),
        fieldsets.METADATA,
        fieldsets.generated_html("abstract_html", "content_html"),
    )
