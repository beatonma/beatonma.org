from django.db import models


class SortableMixin(models.Model):
    class Meta:
        abstract = True
        ordering = ["sort_order"]

    sort_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
        db_index=True,
    )
