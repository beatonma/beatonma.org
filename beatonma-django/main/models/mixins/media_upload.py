import logging
import os
import re
from pathlib import Path

from django.conf import settings
from django.db import models
from django.db.models import QuerySet

log = logging.getLogger(__name__)


VIDEO_PATTERN = re.compile(r".*\.(mp4|webm)$")
AUDIO_PATTERN = re.compile(r".*\.(mp3|wav)$")
IMAGE_PATTERN = re.compile(r".*\.(jpe?g|png|svg|webp)$")
TEXT_PATTERN = re.compile(r".*\.(md|txt)$")


class MediaType(models.TextChoices):
    Audio = "audio"
    Video = "video"
    Image = "image"
    Text = "text"
    Unknown = "unknown"

    @classmethod
    def from_filename(cls, filename: str) -> "MediaType":
        if IMAGE_PATTERN.match(filename):
            return MediaType.Image
        if VIDEO_PATTERN.match(filename):
            return MediaType.Video
        if AUDIO_PATTERN.match(filename):
            return MediaType.Audio
        if TEXT_PATTERN.match(filename):
            return MediaType.Text
        return MediaType.Unknown


class UploadedMediaQuerySet(QuerySet):
    def delete(self):
        for resource in self.all():
            resource.delete_uploaded_files()
        super().delete()


class UploadedMediaMixin(models.Model):
    class Meta:
        abstract = True

    queryset_class = UploadedMediaQuerySet

    file: models.FileField
    uploaded_file_fields = ("file",)

    def delete(self, *args, **kwargs):
        self.delete_uploaded_files()
        super().delete(*args, **kwargs)

    def delete_uploaded_files(self):
        for field_name in self.uploaded_file_fields:
            field = getattr(self, field_name)
            if field:
                try:
                    os.remove(field.path)
                    log.warning(f"Deleted file {field.path}")
                except FileNotFoundError:
                    log.warning(f"File already deleted or moved: {field.path}")
            else:
                log.warning(
                    f"No file associated with field '{field_name}' on model {self}"
                )

    @classmethod
    def move_filesystem_file(
        cls,
        source_path: str,
        target_root: str,
        *,
        source_root: str,
    ):
        """Returns the new target path, relative to settings.MEDIA_ROOT.

        The resulting path will have the same relative path to target_root as the
        source had to sources_root."""
        absolute_source = Path(settings.MEDIA_ROOT, source_path)
        source_root = os.path.join(settings.MEDIA_ROOT, source_root)
        relative_source = os.path.relpath(absolute_source, source_root)
        if ".." in relative_source:
            raise ValueError(
                f"source_root must be an ancestor of source_path: root={source_root}, path={source_path}"
            )

        absolute_target = Path(settings.MEDIA_ROOT, target_root, relative_source)

        source_exists = absolute_source.exists()
        target_exists = absolute_target.exists()

        if (not source_exists) and target_exists:
            log.info(
                f"File appears to have moved already: {absolute_source} -> {absolute_target}"
            )

        elif not source_exists:
            raise FileNotFoundError(f"Source file does not exist: {absolute_source}")

        else:
            log.info(f"Moving file {absolute_source} -> {absolute_target}")
            os.makedirs(os.path.dirname(absolute_target), exist_ok=True)
            os.rename(absolute_source, absolute_target)

        return str(absolute_target.relative_to(settings.MEDIA_ROOT))
