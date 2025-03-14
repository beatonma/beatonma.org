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
