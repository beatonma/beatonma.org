import logging

from django.db.models import Count
from taggit.models import Tag

log = logging.getLogger(__name__)


def cleanup():
    """Remove any 'dangling' objects from the database.

    Currently, just removes tags which are no longer attached to anything."""
    unused_tags = Tag.objects.annotate(
        item_count=Count("taggit_taggeditem_items")
    ).filter(item_count=0)

    if unused_tags.exists():
        log.info(f"Deleting {unused_tags.count()} unused tag(s):")
        for tag in unused_tags:
            log.info(f"- {tag.name}")
        unused_tags.delete()
