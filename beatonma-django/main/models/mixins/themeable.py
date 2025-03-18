from typing import Optional

from colorfield.fields import ColorField
from django.db import models


class ThemeableMixin(models.Model):
    class Meta:
        abstract = True

    SAMPLE_COLORS = [
        ("#ee4545", "#ee4545"),
        ("#0e70b8", "#0e70b8"),
        ("#16b06b", "#16b06b"),
        ("#823dae", "#823dae"),
        ("#e13255", "#e13255"),
        ("#fdf472", "#fdf472"),
        ("#d86900", "#d86900"),
        ("#636363", "#636363"),
        ("#ff6d60", "#ff6d60"),
        ("#f7d060", "#f7d060"),
        ("#f3e99f", "#f3e99f"),
        ("#98d8aa", "#98d8aa"),
        ("#3c486b", "#3c486b"),
        ("#f0f0f0", "#f0f0f0"),
        ("#f9d949", "#f9d949"),
        ("#f45050", "#f45050"),
        ("#4d455d", "#4d455d"),
        ("#e96479", "#e96479"),
        ("#f5e9cf", "#f5e9cf"),
        ("#7db9b6", "#7db9b6"),
        ("#0a4d68", "#0a4d68"),
        ("#088395", "#088395"),
        ("#05bfdb", "#05bfdb"),
        ("#00ffca", "#00ffca"),
        ("#2c3333", "#2c3333"),
        ("#2e4f4f", "#2e4f4f"),
        ("#0e8388", "#0e8388"),
        ("#cbe4de", "#cbe4de"),
        ("#181823", "#181823"),
        ("#537fe7", "#537fe7"),
        ("#c0eef2", "#c0eef2"),
        ("#e9f8f9", "#e9f8f9"),
        ("#483838", "#483838"),
        ("#42855b", "#42855b"),
        ("#90b77d", "#90b77d"),
        ("#d2d79f", "#d2d79f"),
    ]

    color_muted = ColorField(blank=True, samples=SAMPLE_COLORS)
    color_vibrant = ColorField(blank=True, samples=SAMPLE_COLORS)

    def get_default_theme_from(self, source: Optional["ThemeableMixin"]):
        if not source:
            return

        if not self.color_muted:
            self.color_muted = source.color_muted

        if not self.color_vibrant:
            self.color_vibrant = source.color_vibrant
