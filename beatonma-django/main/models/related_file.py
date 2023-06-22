from common.models import ApiModel, BaseModel
from common.models.generic import GenericFkMixin
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from main.forms import SanitizedFileField
from main.util import get_media_type_description, to_absolute_url


class RelatedFile(GenericFkMixin, ApiModel, BaseModel):
    """Files that are uploaded"""

    file = SanitizedFileField(
        blank=True,
        upload_to="related/%Y/",
        filename_attrs=["description"],
    )
    original_filename = models.CharField(
        max_length=1024,
        editable=False,
        null=True,
    )

    description = models.CharField(
        max_length=140,
        blank=True,
        null=True,
        help_text="File content description",
    )

    def url(self):
        return self.file.url

    def to_json(self) -> dict:
        return {
            "url": to_absolute_url(self.file.url),
            "description": self.description,
            "type": get_media_type_description(self),
        }

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.original_filename = self.file.name

        super().save(force_insert, force_update, using, update_fields)

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
