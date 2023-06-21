from django.db import models

from common.models import BaseModel


class CeleryTaskTest(BaseModel):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f"CeleryTaskTest({self.name})"
