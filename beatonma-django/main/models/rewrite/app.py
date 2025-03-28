import os

from common.models import BaseModel
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from main.models import Link
from main.models.mixins.media_upload import UploadedMediaMixin
from main.storage import OverwriteStorage

from .post import BasePost


class AppPost(BasePost):
    codename = models.CharField(max_length=255, unique=True)
    repository = models.OneToOneField(
        "github.GithubRepository",
        on_delete=models.CASCADE,
        related_name="app_post",
        null=True,
        blank=True,
    )
    icon = models.OneToOneField(
        "UploadedFile",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )

    script = models.ForeignKey(
        "AppResource",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )

    def build_slug(self):
        return slugify(self.codename)

    def get_absolute_url(self) -> str:
        return reverse("app_post", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._update_repository_link()

    def _update_repository_link(self):
        if not self.repository:
            return
        ct = ContentType.objects.get_for_model(self)
        if self.repository.is_public():
            Link.objects.update_or_create(
                url=self.repository.url,
                content_type=ct,
                object_id=self.pk,
                defaults={"description": "source"},
            )
        else:
            Link.objects.filter(
                url=self.repository.url,
                content_type=ct,
                object_id=self.pk,
            ).delete()

    def resource_directory(self):
        return f"apps/{self.slug}"


class ChangelogPost(BasePost):
    is_publishable_dependencies = ("app",)
    app = models.ForeignKey(
        AppPost,
        on_delete=models.CASCADE,
        related_name="changelogs",
    )
    version = models.CharField(max_length=32)

    def build_slug(self):
        return slugify(f"{self.app.codename}-{self.version}".replace(".", "-"))

    def get_absolute_url(self) -> str:
        return f"{self.app.get_absolute_url()}#{self.version}"


def appresource_upload_to(instance: "AppResource", filename: str):
    return os.path.join(instance.app.resource_directory(), filename)


class AppResource(UploadedMediaMixin, BaseModel):
    app = models.ForeignKey(
        AppPost,
        on_delete=models.CASCADE,
        related_name="resources",
    )
    file = models.FileField(
        upload_to=appresource_upload_to,
        storage=OverwriteStorage(),
    )

    def save(self, *args, **kwargs):
        created = not self.pk

        super().save(*args, **kwargs)

        if created:
            if self.file.name.endswith(".zip"):
                self.extract_zip(self.file)
                self.delete()
                return
            self.app.save()

    def extract_zip(self, file):
        from zipfile import ZipFile

        resource_dir = self.app.resource_directory()
        absolute_resource_dir = os.path.join(settings.MEDIA_ROOT, resource_dir)

        with ZipFile(file, "r") as contents:
            contents.extractall(absolute_resource_dir)
            extracted_files = contents.filelist

        for f in extracted_files:
            path = os.path.join(resource_dir, f.filename)
            if path == file.path:
                continue
            if os.path.isdir(os.path.join(settings.MEDIA_ROOT, path)):
                continue
            AppResource.objects.get_or_create(app=self.app, file=path)

    def __str__(self):
        return f"{self.app.slug}/{self.file.name}"
