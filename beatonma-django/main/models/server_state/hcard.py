from common import microformats
from common.models import BaseModel
from common.models.singleton import Singleton
from django.db import models
from main.models.link import LinkedMixin
from main.models.mixins.cache import GlobalStateCacheMixin


class SiteHCard(GlobalStateCacheMixin, LinkedMixin, Singleton, BaseModel):
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

    def __str__(self):
        return "Site h-card singleton"
