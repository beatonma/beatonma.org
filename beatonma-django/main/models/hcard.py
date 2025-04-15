from common.models import BaseModel
from common.models.singleton import Singleton
from django.db import models


class SiteHCard(Singleton, BaseModel):
    html = models.TextField()

    def __str__(self):
        return "Site h-card singleton"
