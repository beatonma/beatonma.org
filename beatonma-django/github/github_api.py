import logging
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Callable

import requests
from common.util import http
from django.conf import settings
from github.models import GithubETag
from github.tasks.util import parse_datetime

log = logging.getLogger(__name__)

_TIMEOUT = 2

_session = requests.Session()


class GithubApiException(Exception):
    pass


@dataclass
class GithubResponseHeaders:
    etag: str
    timestamp: datetime


def _prepare_request(url: str, params: dict, headers: dict) -> requests.PreparedRequest:
    return requests.Request("GET", url, params=params, headers=headers).prepare()


def _get(request: requests.PreparedRequest) -> requests.Response:
    return _session.send(request)


def get_if_changed(url, params=None, headers=None) -> requests.Response:
    """If data has not changed since the last time we asked, return None."""

    if params is None:
        params = {}

    if headers is None:
        headers = {}

    headers.update(
        {
            "Authorization": f"token {settings.GITHUB_ACCESS_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": settings.GITHUB_USERNAME,
        }
    )

    request = _prepare_request(url, params=params, headers=headers)
    previous_etag = _get_existing_etag(request.url)

    if previous_etag:
        request.headers.update({"If-None-Match": previous_etag.etag})

    response = _get(request)

    log.info(f"[{response.status_code}] {url}")

    if response.status_code == 304:  # HTTP 304 Not Modified
        return response

    elif response.status_code != 200:
        raise GithubApiException(
            f"Unexpected status code [{response.status_code}]: {url} | {response}"
        )

    response_headers = _parse_response_headers(response.headers)
    _remember(request.url, response_headers)

    return response


def for_each(
    url,
    block: Callable[[dict], None],
    params=None,
    headers=None,
) -> requests.Response:
    """Run [block] with each object in the response list of data."""

    response = get_if_changed(url, params, headers)

    if response.status_code == http.STATUS_304_NOT_MODIFIED:
        return response

    data: list[dict] | None = response.json()

    while data is not None:
        for obj in data:
            block(obj)

        next_page_link = response.links.get("next")
        if next_page_link:
            time.sleep(0.5)
            response = get_if_changed(next_page_link.get("url"), headers=headers)

            if response.status_code == http.STATUS_304_NOT_MODIFIED:
                break

            data = response.json()

        else:
            break

    return response


def _get_existing_etag(url: str) -> GithubETag | None:
    try:
        return GithubETag.objects.get(url=url)
    except GithubETag.DoesNotExist:
        pass


def _remember(url: str, headers: GithubResponseHeaders):
    GithubETag.objects.update_or_create(
        url=url,
        defaults={
            "etag": headers.etag,
            "timestamp": headers.timestamp,
        },
    )


def _parse_response_headers(headers) -> GithubResponseHeaders:
    etag: str = headers["ETag"]
    timestamp = parse_datetime(headers["Date"])

    return GithubResponseHeaders(etag, timestamp)
