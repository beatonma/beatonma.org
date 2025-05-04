import logging

from common.admin import BaseAdmin
from django.contrib import admin
from main.admin.util import media_preview
from main.models.related_file import RelatedFile, UploadedFile

log = logging.getLogger(__name__)


@admin.register(UploadedFile)
class UploadedFileAdmin(BaseAdmin):
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
class RelatedFileAdmin(UploadedFileAdmin):
    editable_fields = UploadedFileAdmin.editable_fields + [
        "sort_order",
    ]
