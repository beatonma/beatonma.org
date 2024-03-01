import os

from common.models import BaseModel
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from main.models.mixins.media_upload import UploadedMediaMixin
from main.storage import OverwriteStorage
from main.views import view_names

WEBAPPS_UPLOAD_PATH = "webapps/"


def _resource_upload_to(instance: "WebappResource", filename):
    """Dynamically resolve directory for webapp."""
    return os.path.join(WEBAPPS_UPLOAD_PATH, instance.webapp.slug, filename)


def _webapp_resource_dir(webapp_name: str):
    return os.path.join(settings.MEDIA_ROOT, WEBAPPS_UPLOAD_PATH, webapp_name)


def _relative_media_path(path: str) -> str:
    return os.path.relpath(path, settings.MEDIA_ROOT)


class WebappResource(UploadedMediaMixin, BaseModel):
    webapp = models.ForeignKey(
        "WebApp",
        on_delete=models.CASCADE,
        related_name="resources",
    )
    file = models.FileField(
        upload_to=_resource_upload_to,
        storage=OverwriteStorage(),
    )

    def save(self, *args, **kwargs):
        created = not self.pk

        super().save(*args, **kwargs)
        if created:
            _notify_resource_added(self.webapp)

    def __str__(self):
        return f"{self.webapp.slug}/{self.file.name}"


class WebApp(UploadedMediaMixin, BaseModel):
    """A simple page with an attached javascript webapp."""

    title = models.CharField(max_length=140)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to=WEBAPPS_UPLOAD_PATH, storage=OverwriteStorage())
    content_html = models.TextField(
        blank=True,
        help_text="The main body of the webapp in HTML",
    )
    inherit_site_theme = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

        if self.resources.all().exists():
            # If webapp has additional resources, move its script from root
            # webapps/ directory to webapps/slug/ directory, alongside resource
            # files.
            f = self.file
            move_to = os.path.join(
                self.resource_directory(),
                os.path.basename(f.name),
            )
            if f.path != move_to:
                os.rename(
                    f.path,
                    move_to,
                )
                self.file = _relative_media_path(move_to)

                super().save(*args, **kwargs)

    def __str__(self):
        return self.slug

    def resource_directory(self):
        return _webapp_resource_dir(self.slug)

    def basename(self) -> str:
        return os.path.basename(self.file.path)

    def get_absolute_url(self):
        return reverse(view_names.WEBAPP, args=[self.slug])

    def _extract_zip(self):
        resource_dir = self.resource_directory()

        from zipfile import ZipFile

        with ZipFile(self.script, "r") as contents:
            contents.extractall(resource_dir)

        for cwd, _, files in os.walk(resource_dir):
            for f in files:
                path = _relative_media_path(os.path.join(cwd, f))
                WebappResource.objects.get_or_create(webapp=self, file=path)


def _notify_resource_added(webapp: WebApp):
    webapp.save()
