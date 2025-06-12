"""Remove any 'dangling' objects from the database.

Currently, just removes tags which are no longer attached to anything."""

from django.core.management import BaseCommand
from taggit.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        self._cleanup_tags()

    def _cleanup_tags(self):
        """Equivalent to remove_orphaned_tags management command."""
        unused_tags = Tag.objects.filter(taggit_taggeditem_items=None)

        if unused_tags.exists():
            self.stdout.write(f"Deleting {unused_tags.count()} unused tag(s):")
            for tag in unused_tags:
                self.stdout.write(f"- {tag.name}")
            unused_tags.delete()
