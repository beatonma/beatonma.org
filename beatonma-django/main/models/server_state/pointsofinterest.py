from common.models import BaseModel, Singleton
from main.models.link import LinkedMixin
from main.models.mixins.cache import GlobalStateCacheMixin


class PointsOfInterest(GlobalStateCacheMixin, LinkedMixin, Singleton, BaseModel):
    def __str__(self):
        return "PointsOfInterest"
