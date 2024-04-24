import logging
from urllib.parse import urljoin

from django.conf import settings

log = logging.getLogger(__name__)


def to_absolute_url(path: str) -> str:
    return urljoin(f"https://{settings.DOMAIN_NAME}", path)
