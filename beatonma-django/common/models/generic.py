from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class GenericFkMixin(models.Model):
    class Meta:
        abstract = True

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target_object = GenericForeignKey("content_type", "object_id")

    @classmethod
    def gfk_field_ct(cls):
        """Return the name of the field used for ContentType of the target object."""
        return "content_type"

    @classmethod
    def gfk_field_pk(cls):
        """Return the name of the field used for primary key of the target object."""
        return "object_id"


def generic_fk(obj: models.Model) -> dict:
    ct = ContentType.objects.get_for_model(obj)
    return {
        GenericFkMixin.gfk_field_ct(): ct,
        GenericFkMixin.gfk_field_pk(): obj.pk,
    }
