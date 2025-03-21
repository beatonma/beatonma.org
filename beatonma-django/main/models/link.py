from typing import Iterable
from urllib.parse import urlparse

from common.models import BaseModel
from common.models.generic import GenericFkMixin
from django.db import models
from django.db.models import UniqueConstraint
from main.models.mixins import StyleableSvgMixin

DESCRIPTION_CHOICES = (
    ("source", "Source"),
    ("install", "Install"),
    ("download", "Download"),
    ("webapp", "Webapp"),
    ("link", "Link"),
)
_description_sort_order = {
    "source": -1,
    "install": 1,
    "download": 1,
    "webapp": 1,
    "link": 4,
}


def sort_links(links: Iterable["Link"]):
    return sorted(
        links,
        key=lambda link: _description_sort_order.get(link.description, 1000),
    )


class LinkQuerySet(models.QuerySet):
    def sorted_by_type(self):
        links = self.all()

        return sort_links(links)


class Link(GenericFkMixin, BaseModel):
    objects = LinkQuerySet.as_manager()
    url = models.URLField(max_length=512)
    description = models.CharField(
        max_length=128,
        choices=DESCRIPTION_CHOICES,
        blank=True,
        null=True,
    )

    host = models.ForeignKey(
        "main.Host",
        on_delete=models.CASCADE,
        related_name="links",
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            if "://" not in self.url:
                self.url = f"https://{self.url}"

            _, netloc, _, _, _, _ = urlparse(self.url)

            if netloc:
                host, _ = Host.objects.get_or_create(
                    domain=netloc,
                    defaults={"name": netloc.removeprefix("www.")},
                )
                self.host = host

        super().save(*args, **kwargs)

    def __str__(self):
        return self.url

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["url", "content_type", "object_id"],
                name="unique_url_per_target",
            )
        ]


class Host(StyleableSvgMixin, BaseModel):
    """Used to show a download/installation/source link."""

    name = models.CharField(max_length=255)
    domain = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique url pattern used for parsing",
    )

    def __str__(self):
        return self.name
