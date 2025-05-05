import logging
from urllib.parse import urljoin, urlparse

from django.conf import settings

log = logging.getLogger(__name__)


def to_absolute_url(path: str) -> str:
    schema = "http" if settings.DEBUG else "https"
    return urljoin(f"{schema}://{settings.DOMAIN_NAME}", path)


def enforce_trailing_slash(url: str) -> str:
    """Ensure that the URL ends with a slash.

    The url may be an absolute URL, or a relative path."""
    scheme, netloc, path, params, query, fragment = urlparse(url)

    if not path.endswith("/"):
        path += "/"

    if scheme:
        url = f"{scheme}://{netloc}{path}"
    else:
        url = path

    if query:
        url += f"?{query}"
    if fragment:
        url += f"#{fragment}"
    return url
