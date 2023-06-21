from common.models import BaseModel
from main.models.mixins import ThemeableMixin


class DevThemePreview(ThemeableMixin, BaseModel):
    def __str__(self):
        colors = list(filter(None, [self.color_muted, self.color_vibrant]))

        if colors:
            return " ".join(colors)

        return f"No colors"
