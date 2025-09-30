import logging
import os
import re
from re import Match
from urllib.parse import urljoin

import navigation
from bs4 import BeautifulSoup
from common.models import BaseModel
from common.models.generic import generic_fk
from common.util import regex
from common.util.pipeline import PipelineItem
from common.util.url import enforce_trailing_slash
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from github.models import GithubRepository
from main.models import Link
from main.models.mixins.media_upload import UploadedMediaMixin
from main.storage import OverwriteStorage

from .post import Post

log = logging.getLogger(__name__)


def _update_repo_link(post: Post, repository: GithubRepository | None):
    if not repository:
        return
    target = generic_fk(post)
    if repository.is_public():
        Link.objects.update_or_create(
            url=repository.url,
            **target,
            defaults={"description": "source"},
        )
    else:
        Link.objects.filter(url=repository.url, **target).delete()


class AppPost(Post):
    class Meta:
        ordering = ("-published_at",)

    default_feeds = Post.default_feeds + [
        ("apps", "Projects"),
    ]

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
    widget_style = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
        help_text=_(
            "Element style applied to the element that wraps the "
            "embedded widget - use to apply a background or padding."
        ),
    )
    widget_data = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
        help_text=_("Optional data passed to widget via URL search params."),
    )
    script_is_widget = models.BooleanField(
        default=False,
        help_text=_(
            "If true, this app can be included as part of a parent UI. "
            "Otherwise it should only displayed as its own window."
        ),
    )

    def build_slug(self):
        return slugify(self.codename)

    def get_absolute_url(self):
        return navigation.app(self.slug)

    def save(self, *args, **kwargs):
        if self.pk:
            previous = AppPost.objects.get(pk=self.pk)
            if self.slug != previous.slug:
                log.warning(f"Slug has changed {previous.slug} -> {self.slug}")
                self.move_resource_directory(
                    previous.resource_directory(), self.resource_directory()
                )

        super().save(*args, **kwargs)
        _update_repo_link(self, self.repository)

    def resource_directory(self):
        return f"apps/{self.slug}"

    def move_resource_directory(self, original_root: str, target_root: str):
        """Migrate files from original_root to target_root, maintaining relative structure."""

        for res in self.resources.all():
            res.move_file(source_root=original_root, target_root=target_root)

        if os.path.exists(original_root) and not os.listdir(original_root):
            os.rmdir(original_root)
            log.info(f"Removed empty directory {original_root}")

    def __str__(self):
        return f"App: {self.title or self.content[:64] or self.slug}"


class ChangelogPost(Post):
    class Meta:
        ordering = ("-published_at",)

    default_feeds = Post.default_feeds + [
        ("changelogs", "Changelogs"),
    ]
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
        _update_repo_link(self, self.app.repository)

    def build_slug(self):
        return slugify(f"{self.app.codename}_{self.version}".replace(".", "-"))

    def get_absolute_url(self):
        return navigation.changelog(self.slug)

    def extra_markdown_processors(self):
        extra = []
        if repo := self.app.repository:
            extra += [
                lambda markdown: self._linkify_github_issues(
                    repo_url=repo.url, markdown=markdown
                ),
            ]

        return super().extra_markdown_processors() + extra

    def extra_html_processors(self) -> list[PipelineItem[BeautifulSoup]]:
        extra = []
        if repo := self.app.repository:
            extra += [
                lambda soup: self._make_github_urls_absolute(
                    repo_url=repo.url, soup=soup
                )
            ]
        return super().extra_html_processors() + extra

    def __str__(self):
        return f"Changelog: {self.app.title} {self.version}"

    @staticmethod
    def _linkify_github_issues(*, repo_url: str, markdown: str) -> str:
        def _sub(match: Match):
            issue = match.group("issue")
            href = urljoin(enforce_trailing_slash(repo_url), f"issues/{issue}")
            return f'<a href="{href}">#{issue}</a>'

        return re.sub(regex.GITHUB_ISSUE, _sub, markdown)

    @staticmethod
    def _make_github_urls_absolute(
        *, repo_url: str, soup: BeautifulSoup
    ) -> BeautifulSoup:
        for a in soup.find_all("a", href=True):
            a["href"] = urljoin(enforce_trailing_slash(repo_url), a["href"])
        return soup


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
        max_length=255,
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

    def move_file(self, *, source_root: str, target_root: str):
        self.file.name = self.move_filesystem_file(
            self.file.name, target_root, source_root=source_root
        )
        self.save()

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
        return f"{self.app.slug} {self.file.name}"
