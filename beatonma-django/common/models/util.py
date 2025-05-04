from typing import Type

from django.apps import apps
from django.db import models


def implementations_of[T: models.Model](mixin: Type[T]) -> list[Type[T]]:
    return [m for m in apps.get_models() if issubclass(m, mixin)]
