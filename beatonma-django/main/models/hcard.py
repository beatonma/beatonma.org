from common import microformats
from common.models import BaseModel
from common.models.singleton import Singleton
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from .link import Link
from .mixins.cache import GlobalStateCacheMixin


class SiteHCard(GlobalStateCacheMixin, Singleton, BaseModel):
    name = models.CharField(max_length=255, help_text=microformats.HCard.p_name)
    url = models.URLField(help_text=microformats.HCard.u_url)

    photo = models.ForeignKey(
        "UploadedFile",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
        help_text=microformats.HCard.u_photo,
    )
    logo = models.ForeignKey(
        "UploadedFile",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
        help_text=microformats.HCard.u_logo,
    )

    locality = models.CharField(
        max_length=255, blank=True, null=True, help_text=microformats.HCard.p_locality
    )
    region = models.CharField(
        max_length=255, blank=True, null=True, help_text=microformats.HCard.p_region
    )
    country = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=microformats.HCard.p_country_name,
    )

    birthday = models.DateField(
        blank=True, null=True, help_text=microformats.HCard.dt_bday
    )

    relme_links = GenericRelation(Link)

    def __str__(self):
        return "Site h-card singleton"
