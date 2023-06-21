import time
from typing import Optional

import requests
from requests.exceptions import ConnectionError

MAX_TRIES = 10

NGINX_URL = "http://nginx-server-tests"

__all__ = [
    "tests",
]


def expect_result(
    path: Optional[str] = None,
    expected_code: int = None,
    url: str = None,
):
    if url is None:
        url = f"{NGINX_URL}{path}"

    for attempts in range(1, MAX_TRIES):
        try:
            result = requests.get(url, timeout=1, allow_redirects=False)
            break
        except ConnectionError as e:
            result = lambda x: print(e)
            result.status_code = 444
            break
        except TimeoutError as e:
            print(f"{e.__class__}: {url}")
            time.sleep(5)
    else:
        raise Exception(f"FAILED: {url} failed too many times")

    assert (
        result.status_code == expected_code
    ), f"URL {url} returned status={result.status_code} [expected {expected_code}]"


def tests():
    expect_result("/health-check/", 200)
    expect_result("/", 200)
    expect_result("/about/", 200)
    expect_result("/ping/", 200)

    expect_result("/somefile.exe", 444)
    expect_result(url="http://prefix.nginx-server-tests/ping/", expected_code=444)
