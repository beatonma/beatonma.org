import logging
import os

from django.db import models
from django.db.models import QuerySet

log = logging.getLogger(__name__)


class UploadedMediaQuerySet(QuerySet):
    def delete(self):
        for resource in self.all():
            resource.delete_file()
        super().delete()


class UploadedMediaMixin(models.Model):
    class Meta:
        abstract = True

    objects = UploadedMediaQuerySet.as_manager()

    file: models.FileField

    def delete(self, *args, **kwargs):
        self.delete_file()
        super().delete(*args, **kwargs)

    def delete_file(self):
        if not self.file:
            log.warning(f"No file associated with model {self}")
            return
        if os.path.exists(self.file.path):
            os.remove(self.file.path)
            log.warning(f"Deleted file {self.file.path}")
