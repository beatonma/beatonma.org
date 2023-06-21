from typing import Type, TypeVar

from django.db import models

Model = TypeVar("Model", bound=models.Model)
ModelType = TypeVar("ModelType", bound=Type[models.Model])
