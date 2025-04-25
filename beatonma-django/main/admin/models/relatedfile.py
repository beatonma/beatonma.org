import logging

from common.admin import BaseAdmin
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.safestring import mark_safe
from main.models.related_file import (
    IMAGE_PATTERN,
    VIDEO_PATTERN,
    RelatedFile,
    UploadedFile,
)

log = logging.getLogger(__name__)


class RelatedFileInline(GenericTabularInline):
    model = RelatedFile
    extra = 1


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
        if not file:
            return None

        if IMAGE_PATTERN.match(file.name):
            return mark_safe(rf'<img src="{file.url}" loading="lazy" />')
        elif VIDEO_PATTERN.match(file.name):
            return mark_safe(
                rf"<video src={file.url} autoplay controls muted loop></video>"
            )
        return None

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
