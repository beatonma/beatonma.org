from common.admin import register_model_to_default_admin as register
from main.models import (
    AppResource,
    Host,
    Link,
    MessageOfTheDay,
    PointsOfInterest,
    SiteHCard,
)

from . import post, theme, uploaded_files
from .inline import LinkInline

# Very simple admin pages may be registered here.
register(AppResource)

register(Link, list_display=["url", "label", "description"])
register(Host, list_display=["name", "domain"])
register(SiteHCard, editable_fields=["*"], inlines=[LinkInline])
register(PointsOfInterest, inlines=[LinkInline])
register(
    MessageOfTheDay,
    editable_fields=["content_html", "public_from", "public_until", "is_published"],
    field_groups=[
        ["public_from", "public_until"],
    ],
)
