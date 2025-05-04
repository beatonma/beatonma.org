from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline
from main.admin.util import media_preview
from main.models import AppResource, Link, RelatedFile


class LinkInline(GenericTabularInline):
    model = Link
    extra = 1


class AppResourceInline(TabularInline):
    model = AppResource
    extra = 1


class RelatedFileInline(GenericStackedInline):
    model = RelatedFile
    extra = 1

    fields = (
        ("file", "get_preview", "thumbnail", "get_thumbnail"),
        ("fit", "description", "sort_order"),
    )
    readonly_fields = ("get_preview", "get_thumbnail")
    preview_style = "max-width:150px;max-height:150px;"

    @admin.display(description="Preview")
    def get_preview(self, related):
        return media_preview(related.file, self.preview_style)

    @admin.display(description="Preview")
    def get_thumbnail(self, related):
        return media_preview(related.thumbnail, self.preview_style)
