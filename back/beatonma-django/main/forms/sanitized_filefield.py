"""
Provides SanitizedFileField which resizes and strips EXIF data from image files
at upload time.

Based on ResizedImageField from django_resized:
  https://github.com/un1t/django-resized/blob/master/django_resized/forms.py
"""
import re
from io import BytesIO
from pathlib import Path
from typing import List, Optional, Tuple, Union

from django.conf import settings
from django.core.files.base import ContentFile, File
from django.db.models import FileField
from PIL import Image, ImageFile

from main.forms import RandomFilename

IMAGE_PATTERN = re.compile(r"(.*)\.(jpg|jpeg|png)")


DEFAULT_SIZE = getattr(settings, "UPLOAD_DEFAULT_IMAGE_SIZE", [2560, 1440])
DEFAULT_QUALITY = getattr(settings, "UPLOAD_DEFAULT_QUALITY", 75)


def rescale_image(
    content: File,
    size: Tuple[int, int] = DEFAULT_SIZE,
    quality: int = DEFAULT_QUALITY,
    outfile: Union[str, Path] = None,
) -> Optional[File]:
    img = Image.open(content.file)

    try:
        resample = Image.Resampling.LANCZOS
    except AttributeError:
        resample = Image.ANTIALIAS

    img.thumbnail(size, resample)
    thumb = img

    img_info = img.info
    if "exif" in img_info:
        img_info.pop("exif")

    ImageFile.MAXBLOCK = max(ImageFile.MAXBLOCK, thumb.size[0] * thumb.size[1])
    img_format = img.format

    if outfile:
        thumb.save(
            outfile,
            format=img_format,
            quality=quality,
            **img_info,
        )
        return

    new_content = BytesIO()
    thumb.save(
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
        filename_literals:  List of literal string values to include at
                            start of randomized filename. Helps with sorting/
                            identifying files in filesystem.
        filename_attrs:     List of attributes of the model which should be
                            used to build the randomized filename. Helps with
                            sorting/identifying files in filesystem.
    """

    attr_class = ResizeFieldFile
    size: Tuple[int, int]
    quality: int

    def __init__(
        self,
        verbose_name=None,
        name=None,
        upload_to: str = "",
        filename_literals: List[str] = None,
        filename_attrs: List[str] = None,
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
