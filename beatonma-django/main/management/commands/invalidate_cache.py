from django.core.management import BaseCommand

from common.models.cache import InvalidateCacheMixin
from common.models.util import implementations_of


class Command(BaseCommand):
    def handle(self, *args, **options):
        cacheable_models = implementations_of(InvalidateCacheMixin)
        for model in cacheable_models:
            model.invalidate_cache()
