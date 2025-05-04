from django.db import models
from django.db.models import QuerySet
from taggit.managers import TaggableManager


class TaggableMixin(models.Model):
    class Meta:
        abstract = True

    tags = TaggableManager(blank=True)

    def get_tags(self) -> QuerySet:
        return self.tags.all().order_by("name")

    def get_tags_list(self) -> list[str]:
        return list(self.get_tags().values_list("name", flat=True))
