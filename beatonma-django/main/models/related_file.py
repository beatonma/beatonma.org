import re

from common.models import ApiModel, BaseModel
from common.models.api import ApiEditable
from common.models.generic import GenericFkMixin
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from main.forms import SanitizedFileField
from main.models.mixins.media_upload import UploadedMediaMixin
from main.util import to_absolute_url

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


class RelatedFile(UploadedMediaMixin, GenericFkMixin, ApiModel, ApiEditable, BaseModel):
    """Files that are uploaded"""

    description_max_length = 140

    file = SanitizedFileField(
        upload_to="related/%Y/",
        filename_attrs=["description"],
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
        max_length=description_max_length,
        blank=True,
        default="",
        help_text="File content description",
    )

    def url(self):
        return self.file.url

    def to_json(self) -> dict:
        return {
            "url": to_absolute_url(self.file.url),
            "description": self.description,
            "type": self.type,
        }

    def save(self, **kwargs):
        if not self.original_filename:
            self.original_filename = self.file.name

        self.type = MediaType.from_filename(self.file.name)
        super().save(**kwargs)

    def __str__(self):
        if self.description:
            return f'{self.file} | "{self.description}"'

        return self.file.name


class RelatedFilesMixin(models.Model):
    class Meta:
        abstract = True

    related_files = GenericRelation(RelatedFile)

    def file_urls(self) -> str:
        return ";".join(self.file_url_list())

    def file_url_list(self) -> list:
        return [x.url() for x in self.related_files.all()]
