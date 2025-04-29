import re
from io import BytesIO
from typing import Callable, Self

import PIL
from common.models import ApiModel, BaseModel
from common.models.api import ApiEditable
from common.models.generic import GenericFkMixin
from django.contrib.contenttypes.fields import GenericRelation
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils import timezone
from main.forms import SanitizedFileField
from main.models.mixins.media_upload import (
    AUDIO_PATTERN,
    IMAGE_PATTERN,
    TEXT_PATTERN,
    VIDEO_PATTERN,
    UploadedMediaMixin,
)
from main.util import to_absolute_url
from PIL import Image

THUMBNAIL_SIZE = (800, 800)


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


def default_upload_to(instance: "BaseUploadedFile", filename) -> str:
    upload_to = instance.__class__.upload_to

    if callable(upload_to):
        return upload_to(instance, filename)

    year = timezone.now().strftime("%Y")
    return f"{upload_to}/{year}/{filename}"


class BaseUploadedFile(UploadedMediaMixin, ApiEditable, BaseModel):
    class Meta:
        abstract = True

    upload_to: str | Callable[[Self, str], str]
    uploaded_file_fields = ("file", "thumbnail")

    class ImageFit(models.TextChoices):
        Cover = "cover"
        Contain = "contain"

    file = SanitizedFileField(
        upload_to=default_upload_to,
        filename_attrs=["description"],
    )
    thumbnail = SanitizedFileField(
        upload_to=default_upload_to,
        filename_attrs=["description"],
        filename_literals=["thumb"],
        size=THUMBNAIL_SIZE,
        blank=True,
        null=True,
    )

    fit = models.CharField(
        max_length=32,
        choices=ImageFit.choices,
        blank=True,
        null=True,
    )
    original_filename = models.CharField(
        max_length=1024,
        editable=False,
        null=True,
    )
    type = models.CharField(
        max_length=10,
        choices=MediaType,
        default=MediaType.Unknown,
    )

    description = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="File content description",
    )

    def file_or_none(self):
        if self.file:
            return self.file

    def thumbnail_or_none(self):
        if self.thumbnail:
            return self.thumbnail

    def url(self):
        return self.file.url

    def save(self, *args, **kwargs):
        if not self.original_filename:
            self.original_filename = self.file.name

        self.type = MediaType.from_filename(self.file.name)

        if not self.thumbnail:
            self.generate_thumbnail(THUMBNAIL_SIZE)
        super().save(*args, **kwargs)

    def generate_thumbnail(self, size: tuple[int, int] | None = None):
        if not self.file or self.type != MediaType.Image:
            return

        try:
            with Image.open(self.file) as img:
                img.thumbnail(size or THUMBNAIL_SIZE)

                thumb_bytes = BytesIO()
                img.save(thumb_bytes, format="webp")
        except PIL.UnidentifiedImageError:
            # Vector images or otherwise unsupported files.
            return

        thumb_name = self.file.name.split(".")[0] + "-thumb.webp"
        thumb_file = InMemoryUploadedFile(
            thumb_bytes,
            field_name=None,
            name=thumb_name,
            content_type="image/webp",
            size=thumb_bytes.tell,
            charset=None,
        )

        self.thumbnail.save(thumb_name, thumb_file, save=False)

    def __str__(self):
        if self.description:
            return f'{self.file} | "{self.description}"'

        return self.file.name


class UploadedFile(BaseUploadedFile):
    upload_to = "uploads"


class RelatedFile(GenericFkMixin, ApiModel, BaseUploadedFile):
    """Files that are uploaded"""

    upload_to = "related"

    sort_order = models.PositiveSmallIntegerField(default=0)

    def to_json(self) -> dict:
        return {
            "url": to_absolute_url(self.file.url),
            "description": self.description,
            "type": self.type,
        }


class RelatedFilesMixin(models.Model):
    class Meta:
        abstract = True

    related_files = GenericRelation(RelatedFile)

    def file_urls(self) -> str:
        return ";".join(self.file_url_list())

    def file_url_list(self) -> list:
        return [x.url() for x in self.related_files.all()]
