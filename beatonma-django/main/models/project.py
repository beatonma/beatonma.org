import logging

from common.models import BaseModel
from django.db import models

log = logging.getLogger(__name__)


class Project(BaseModel):
    """
    Used to organise posts that are about the same piece of work.
    Apps can associate themselves with a project, which can then be used
    to group related apps together.
    """

    name = models.CharField(max_length=255, help_text="A name for this project")
    project_id = models.CharField(
        max_length=255, unique=True, help_text="A unique identifier for this project"
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.project_id
