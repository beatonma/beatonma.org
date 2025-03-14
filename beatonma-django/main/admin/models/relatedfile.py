import logging
import os
import re

from common.admin import BaseAdmin
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html
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


@admin.register(RelatedFile)
class RelatedFileAdmin(BaseAdmin):
    readonly_fields = [
        "original_filename",
        "type",
        "content_type",
        "object_id",
        "file_preview",
        "target_object",
    ]

    def file_preview(self, obj):
        if IMAGE_PATTERN.match(obj.file.name):
            return format_html(rf"<img src={obj.file.url}/>")

        if VIDEO_PATTERN.match(obj.file.name):
            return format_html(
                rf"<video src={obj.file.url} autoplay controls muted loop></video>"
            )

        else:
            log.warning(f"Unhandled file_preview: {obj}")

    def filename(self, obj):
        return os.path.basename(obj.file.name)

    list_display = [
        "filename",
        "type",
        "target_object",
        "created_at",
    ]

    ordering = [
        "file",
    ]

    sortable_by = [
        "created_at",
    ]

    fields = (
        "file_preview",
        "file",
        "thumbnail",
        "fit",
        "type",
        "description",
        "original_filename",
        "target_object",
        "content_type",
        "object_id",
    )


@admin.register(UploadedFile)
class UploadedFileAdmin(BaseAdmin):
    pass
