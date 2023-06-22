from common.models import BaseModel
from django.db import models


class Wurd(BaseModel):
    day = models.PositiveSmallIntegerField(unique=True)
    wurd = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return f"[{self.day}] {self.wurd}"

    class Meta:
        ordering = ["-day"]


class ValidWurd(BaseModel):
    wurd = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.wurd

    class Meta:
        ordering = ["wurd"]
