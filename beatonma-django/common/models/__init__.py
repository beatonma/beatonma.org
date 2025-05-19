from typing import Self, Type

from django.db import models
from django.db.models.base import ModelBase
from django.utils import timezone


class _BaseModelMeta(ModelBase):
    def __new__(cls, name, bases, attrs, **kwargs):
        model_class = super().__new__(cls, name, bases, attrs, **kwargs)

        if "objects" in attrs:
            # Don't change anything if model defines its own 'objects' manager.
            return model_class

        model_class.add_to_class(
            "objects", cls._generate_manager_from_mixins(cls, model_class, bases)
        )
        return model_class

    def _generate_manager_from_mixins(cls, model_class, bases):
        """Create a QuerySet class which inherits from all the queryset classes
        referenced by its mixin classes. This removes the need to manually maintain
        a corresponding chain of queryset inheritance whenever we use a model mixin.

        A mixin model can define a QuerySet class by its "queryset_class" attribute.
        That queryset class can define filters of its own or extend other queryset
        class(es).

        If one of the queryset classes extends from another, the parent class will
        be ignored so that any overriding methods from the child work correctly
        on the generated class."""

        seen = set()

        def get_bases(_bases):
            result = []
            for c in _bases:
                if c == models.Model:
                    continue
                if c in seen:
                    continue
                seen.add(c)
                result.append(c)
                result += get_bases(c.__bases__)
            return result

        mixins = get_bases(bases)

        mixin_queryset_classes = [
            mixin.queryset_class
            for mixin in [model_class] + mixins
            if hasattr(mixin, "queryset_class")
            and issubclass(mixin.queryset_class, models.QuerySet)
        ]

        # Filter out any classes which are subclassed by another class.
        qs_mixins = []

        for x in mixin_queryset_classes:
            is_subclass = False
            for y in mixin_queryset_classes:
                if x is y:
                    continue
                if issubclass(y, x):
                    is_subclass = True
                    break
            if not is_subclass and x not in qs_mixins:
                qs_mixins.append(x)

        class CombinedQuerySet(*qs_mixins, models.QuerySet):
            pass

        return CombinedQuerySet.as_manager()


class BaseModel(models.Model, metaclass=_BaseModelMeta):
    """Provides created_at field with default ordering."""

    # objects: Configured in metaclass

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
from .singleton import Singleton
from .sortable import SortableMixin
from .taggable import TaggableMixin
