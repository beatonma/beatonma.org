import logging
import os

from django.db import models
from django.db.models import QuerySet

log = logging.getLogger(__name__)


class UploadedMediaQuerySet(QuerySet):
    def delete(self):
        for resource in self.all():
            resource.delete_uploaded_files()
        super().delete()


class UploadedMediaMixin(models.Model):
    class Meta:
        abstract = True

    objects = UploadedMediaQuerySet.as_manager()

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

        # if not self.file:
        #     log.warning(f"No file associated with model {self}")
        #     return
        # if os.path.exists(self.file.path):
        #     os.remove(self.file.path)
        #     log.warning(f"Deleted file {self.file.path}")
