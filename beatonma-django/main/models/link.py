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


class Link(GenericFkMixin, BaseModel):
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

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        if not self.pk:
            if "://" not in self.url:
                self.url = f"https://{self.url}"

            parsed = urlparse(self.url)
            scheme, netloc, path, params, query, fragment = parsed

            if netloc:
                host, _ = Host.objects.get_or_create(
                    domain=netloc,
                    defaults={"name": netloc},
                )
                self.host = host

        super().save(force_insert, force_update, using, update_fields)

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

    name = models.CharField(max_length=30)
    domain = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique url pattern used for parsing",
    )

    def __str__(self):
        return self.name
