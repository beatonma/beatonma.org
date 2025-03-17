import logging
import os

from django.conf import settings
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver
from main.models.mixins.media_upload import UploadedMediaMixin

log = logging.getLogger(__name__)


@receiver(pre_delete)
def delete_dereferenced_file(sender, instance, **kwargs):
    if not isinstance(instance, UploadedMediaMixin):
        return

    instance.delete_uploaded_files()


@receiver(post_delete)
def cleanup_unused_media_directories(sender, instance, **kwargs):
    """When a file is deleted, check for"""
    if not isinstance(instance, UploadedMediaMixin):
        return

    for cwd, dirs, files in os.walk(settings.MEDIA_ROOT):
        for d in dirs:
            path: str = os.path.join(cwd, d)
            if not os.listdir(path):
                log.warning(f"Deleting empty directory: {path}")
                os.rmdir(path)
