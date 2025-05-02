import logging

from common.admin import BaseAdmin
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from main.admin.util import media_preview
from main.models.related_file import RelatedFile, UploadedFile

log = logging.getLogger(__name__)


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


@admin.register(UploadedFile)
class BaseUploadedFileAdmin(BaseAdmin):
    editable_fields = [
        "file",
        "thumbnail",
        "description",
        "fit",
    ]
    field_groups = [
        ("file", "_field_file_preview"),
        ("thumbnail", "_field_thumbnail_preview"),
    ]

    def _preview(self, file):
        return media_preview(file)

    @admin.display(description="Preview")
    def _field_file_preview(self, obj):
        return self._preview(obj.file)

    @admin.display(description="Preview")
    def _field_thumbnail_preview(self, obj):
        return self._preview(obj.thumbnail)


@admin.register(RelatedFile)
class RelatedFileAdmin(BaseUploadedFileAdmin):
    editable_fields = BaseUploadedFileAdmin.editable_fields + [
        "sort_order",
    ]
