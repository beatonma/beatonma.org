import os

from common.models import BaseModel
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from main.models import Link
from main.models.formats.markdown import linkify_github_issues
from main.models.mixins.media_upload import UploadedMediaMixin
from main.storage import OverwriteStorage

from .post import Post


class AppPost(Post):
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
    script_html = models.TextField(blank=True, null=True)
    script_is_widget = models.BooleanField(
        default=False,
        help_text=_(
            "If true, this app can be included as part of a parent UI. "
            "Otherwise it should only displayed as its own window."
        ),
    )

    def build_slug(self):
        return slugify(self.codename)

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

    def __str__(self):
        return f"App: {self.title or self.content[:64] or self.slug}"


class ChangelogPost(Post):
    is_publishable_dependencies = ("app",)
    app = models.ForeignKey(
        AppPost,
        on_delete=models.CASCADE,
        related_name="changelogs",
    )
    version = models.CharField(max_length=32)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.title = f"{self.app.title}: {self.version}"
        super().save(*args, **kwargs)

    def build_slug(self):
        return slugify(f"{self.app.codename}_{self.version}".replace(".", "-"))

    def extra_markdown_processors(self):
        extra = []
        if repo := self.app.repository:
            extra.append(
                lambda markdown: linkify_github_issues(
                    repo_url=repo.url, markdown=markdown
                )
            )

        return extra + super().extra_markdown_processors()

    def __str__(self):
        return f"Changelog: {self.app.title} {self.version}"


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
