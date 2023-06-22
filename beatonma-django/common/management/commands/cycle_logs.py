import logging
from datetime import timedelta

from django.core.management import BaseCommand

from common.tasks.cycle_logs import cycle_logs

log = logging.getLogger(__name__)


class Command(BaseCommand):
    """Delete instances of PageView that are older than 30 days.

    This should be scheduled to run at least once per day."""

    def handle(self, *args, **options):
        older_than = timedelta(days=30)
        deleted_count, _ = cycle_logs(older_than=older_than)
        log.info(f"Deleted {deleted_count} PageView objects older than {older_than}.")
