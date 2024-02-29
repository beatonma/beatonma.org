from common.models import BaseModel
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from main.storage import OverwriteStorage
from main.views import view_names


class WebApp(BaseModel):
    """A simple page with an attached javascript webapp."""

    title = models.CharField(max_length=140)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    script = models.FileField(upload_to="webapps/", storage=OverwriteStorage())
    content_html = models.TextField(
        blank=True,
        help_text="The main body of the webapp in HTML",
    )
    inherit_site_theme = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse(view_names.WEBAPP, kwargs={"slug": self.slug})
