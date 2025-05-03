from common.models import BaseModel
from common.models.singleton import Singleton
from main.models.link import LinkedMixin
from main.models.mixins.cache import GlobalStateCacheMixin


class PointsOfInterest(GlobalStateCacheMixin, LinkedMixin, Singleton, BaseModel):
    pass
