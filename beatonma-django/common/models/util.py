from typing import List, Type

from common.models.types import Model
from django.apps import apps


def implementations_of(mixin: Type[Model]) -> List[Type[Model]]:
    return [m for m in apps.get_models() if issubclass(m, mixin)]
