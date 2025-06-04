from io import BytesIO
from typing import Callable, Self

import PIL
from common.models import BaseModel, SortableMixin
from common.models.api import ApiEditable
from common.models.generic import GenericFkMixin
from django.contrib.contenttypes.fields import GenericRelation
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils import timezone
from main.forms import SanitizedFileField
from main.models.formats import Formats
from main.models.mixins.media_upload import MediaType, UploadedMediaMixin
from PIL import Image

THUMBNAIL_SIZE = (800, 800)


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
        choices=MediaType.choices,
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
        return None

    def thumbnail_or_none(self):
        if self.thumbnail:
            return self.thumbnail
        return None

    def url(self):
        return self.file.url

    def save(self, *args, **kwargs):
        if not self.original_filename:
            self.original_filename = self.file.name

        self.type = MediaType.from_filename(self.file.name)
        if self.description:
            self.description = Formats.to_html(self.description)

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


class RelatedFile(SortableMixin, GenericFkMixin, BaseUploadedFile):
    """Files for display alongside a Post or similar content."""

    upload_to = "related"


class RelatedFilesMixin(models.Model):
    class Meta:
        abstract = True

    related_files = GenericRelation(RelatedFile)
