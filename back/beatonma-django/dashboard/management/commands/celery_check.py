import logging

from dashboard.tasks.check_celery import check_celery_works
from django.core.management import BaseCommand

log = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        print("crontest command ran successfully!")

        result = check_celery_works()

        if result.success:
            log.info(result.message)
        else:
            log.warning(result.message)
