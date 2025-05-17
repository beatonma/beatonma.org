from common.models import BaseModel
from django.db.models import QuerySet


class SingletonError(Exception):
    pass


class SingletonQuerySet(QuerySet):
    def get(self, *args, **kwargs):
        return self.first()

    def singleton(self):
        return self.first()


class Singleton(BaseModel):
    class Meta:
        abstract = True

    queryset_class = SingletonQuerySet

    def save(self, *args, **kwargs):
        if (not self.pk) and self.__class__.objects.all().exists():
            raise SingletonError(
                "Cannot create a new instance of singleton model "
                f"'{self.__class__.__name__}' because one already exists!"
            )
        super().save(*args, **kwargs)
