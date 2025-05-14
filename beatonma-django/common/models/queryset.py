from typing import Type

from common.models.util import implementations_of
from django.db import models
from django.db.models import QuerySet


class ExtendedModelQuerySet(QuerySet):
    def exclude_subclasses_of[T: models.Model](self, base_class: Type[T]):
        subclass_related_names = [
            x.__name__.lower()
            for x in implementations_of(base_class)
            if x != base_class
        ]
        exclude_subclasses = {
            f"{subclass}__isnull": True for subclass in subclass_related_names
        }
        return self.filter(**exclude_subclasses)
