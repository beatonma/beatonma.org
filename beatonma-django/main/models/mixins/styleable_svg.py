import logging

from django.core.exceptions import ValidationError
from django.db import models

log = logging.getLogger(__name__)


def validate_svg(value):
    import os.path

    ext = os.path.splitext(value.name)[1]
    log.info(f"File extension: {ext}")
    if ext != ".svg":
        raise ValidationError("This field only accepts SVG files!")


class StyleableSvgMixin(models.Model):
    class Meta:
        abstract = True

    icon_file = models.FileField(
        blank=True,
        validators=[validate_svg],
        upload_to="icon/",
        help_text="SVG icon",
    )
    icon_svg = models.CharField(
        max_length=8192,
        blank=True,
        help_text="<svg> element",
    )

    def clean(self):
        try:
            f = self.icon_file
            if f:
                self.icon_svg = f.read().decode("utf-8")
        except Exception as e:
            log.error(e)

        super().clean()
