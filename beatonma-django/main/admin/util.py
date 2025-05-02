from django.utils.safestring import mark_safe
from main.models.mixins.media_upload import IMAGE_PATTERN, VIDEO_PATTERN


def media_preview(file, style=""):
    if not file:
        return None

    if IMAGE_PATTERN.match(file.name):
        return mark_safe(rf'<img src="{file.url}" loading="lazy" style="{style}" />')

    elif VIDEO_PATTERN.match(file.name):
        return mark_safe(
            rf'<video src={file.url} style="{style}" autoplay controls muted loop></video>'
        )
    return None
