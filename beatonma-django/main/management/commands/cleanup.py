"""Remove any 'dangling' objects from the database.

Currently, just removes tags which are no longer attached to anything."""

from django.core.management import BaseCommand
from django.db.models import Count
from taggit.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        _cleanup()


def _cleanup():
    """Remove any 'dangling' objects from the database.

    Currently, just removes tags which are no longer attached to anything."""
    unused_tags = Tag.objects.annotate(
        item_count=Count("taggit_taggeditem_items")
    ).filter(item_count=0)

    if unused_tags.exists():
        print(f"Deleting {unused_tags.count()} unused tag(s):")
        for tag in unused_tags:
            print(f"- {tag.name}")
        unused_tags.delete()
