from typing import Self, Type

from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """Provides created_at field with default ordering."""

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    def update(self, **kwargs) -> Self:
        if self._state.adding:
            raise self.DoesNotExist

        changed_keys = []
        for key, value in kwargs.items():
            if getattr(self, key) != value:
                setattr(self, key, value)
                changed_keys.append(key)

        self.save(update_fields=changed_keys)
        return self

    @classmethod
    def qualified_name(cls):
        return f"{cls._meta.app_label}.{cls.__name__}"

    @classmethod
    def subclasses(cls) -> list[Type[Self]]:
        from django.apps import apps

        return [m for m in apps.get_models() if issubclass(m, cls)]

    @classmethod
    def fields(cls) -> list[str]:
        return [field.name for field in cls._meta.get_fields()]

    @classmethod
    def local_fields(cls) -> list[str]:
        return [field.name for field in cls._meta.get_fields() if not field.is_relation]

    class Meta:
        abstract = True
        ordering = ["-created_at"]


from .published import PublishedMixin
from .search import SearchMixin
from .taggable import TaggableMixin
