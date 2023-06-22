from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class GenericFkMixin(models.Model):
    class Meta:
        abstract = True

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target_object = GenericForeignKey("content_type", "object_id")


def generic_fk(obj: models.Model) -> dict:
    ct = ContentType.objects.get_for_model(obj)
    return {
        "content_type": ct,
        "object_id": obj.pk,
    }
