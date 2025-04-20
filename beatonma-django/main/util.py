import logging
from urllib.parse import urljoin

from django.conf import settings

log = logging.getLogger(__name__)


def to_absolute_url(path: str) -> str:
    schema = "http" if settings.DEBUG else "https"
    return urljoin(f"{schema}://{settings.DOMAIN_NAME}", path)
