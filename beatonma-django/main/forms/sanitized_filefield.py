"""
Provides SanitizedFileField which resizes and strips EXIF data from image files
at upload time.

Based on ResizedImageField from django_resized:
  https://github.com/un1t/django-resized/blob/master/django_resized/forms.py
"""

import re
from io import BytesIO
from pathlib import Path
from typing import Callable

from django.conf import settings
from django.core.files.base import ContentFile, File
from django.db.models import FileField
from main.forms import RandomFilename
from PIL import Image, ImageFile

IMAGE_PATTERN = re.compile(r"(.*)\.(jpg|jpeg|png)")


DEFAULT_SIZE = getattr(settings, "UPLOAD_DEFAULT_IMAGE_SIZE", [2560, 2560])
DEFAULT_QUALITY = getattr(settings, "UPLOAD_DEFAULT_QUALITY", 75)


def rescale_image(
    content: File,
    size: tuple[int, int] = None,
    quality: int = DEFAULT_QUALITY,
    outfile: str | Path = None,
) -> File | None:
    if size is None:
        size = DEFAULT_SIZE

    resample = Image.Resampling.LANCZOS

    with Image.open(content.file) as img:
        img.thumbnail(size, resample)
        img_format = img.format
        img_info = img.info

        if "exif" in img_info:
            img_info.pop("exif")

        ImageFile.MAXBLOCK = max(ImageFile.MAXBLOCK, img.size[0] * img.size[1])

        if outfile:
            img.save(
                outfile,
                format=img_format,
                quality=quality,
                **img_info,
            )
            return

        new_content = BytesIO()
        img.save(
            new_content,
            format=img_format,
            quality=quality,
            **img_info,
        )
        return ContentFile(new_content.getvalue())


class ResizeFieldFile(FileField.attr_class):
    def save(self, name: str, content: File, save: bool = True):
        if IMAGE_PATTERN.match(name):
            content = rescale_image(content, self.field.size, self.field.quality)

        super().save(name, content, save)


class SanitizedFileField(FileField):
    """
    A FileField that strips image metadata and mangles filenames on upload.

    Attributes:
        filename_literals:  list of literal string values to include at
                            start of randomized filename. Helps with sorting/
                            identifying files in filesystem.
        filename_attrs:     list of attributes of the model which should be
                            used to build the randomized filename. Helps with
                            sorting/identifying files in filesystem.
    """

    attr_class = ResizeFieldFile
    size: tuple[int, int]
    quality: int

    def __init__(
        self,
        verbose_name=None,
        name=None,
        upload_to: str | Callable = "",
        filename_literals: list[str] = None,
        filename_attrs: list[str] = None,
        storage=None,
        **kwargs,
    ):
        self.size = kwargs.pop("size", DEFAULT_SIZE)
        self.quality = kwargs.pop("quality", DEFAULT_QUALITY)

        if isinstance(upload_to, str):
            upload_to = RandomFilename(
                upload_to,
                filename_literals=filename_literals or [],
                filename_attrs=filename_attrs or [],
            )

        super().__init__(verbose_name, name, upload_to, storage, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        for custom_kwarg in ["size", "quality"]:
            kwargs[custom_kwarg] = getattr(self, custom_kwarg)
        return name, path, args, kwargs
