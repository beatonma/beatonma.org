from common.models import BaseModel
from django.db import models
from django.db.models import QuerySet
from main.models.posts.formats import FormatMixin, Formats
from main.models.related_file import RelatedFilesMixin


class AboutQuerySet(QuerySet):
    def get_current(self):
        return self.filter(active=True).order_by("-created_at").first()


class About(
    FormatMixin,
    RelatedFilesMixin,
    BaseModel,
):
    """A 'soft' singleton model for self profile info.

    Exactly one instance of About must be 'active' at a time.
    Setting one instance as active automatically deactivates all others."""

    objects = AboutQuerySet.as_manager()

    description = models.CharField(max_length=1024, help_text="Only visible in admin")
    active = models.BooleanField(default=True)

    content = models.TextField(default="")
    content_html = models.TextField(blank=True, default="", editable=False)

    def get_absolute_url(self):
        return "/about/"

    def save_text(self):
        self.content_html = Formats.to_html(self.format, self.content)

    def save(self, *args, **kwargs):
        if self.active:
            About.objects.filter(active=True).update(active=False)
        else:
            objs = About.objects.exclude(pk=self.pk).filter(active=True)
            if objs.count() != 1:
                raise Exception("No 'about' page is active!")

        self.save_text()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "About"
        verbose_name_plural = "About"
