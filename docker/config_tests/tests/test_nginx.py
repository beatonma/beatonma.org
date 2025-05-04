import time
from urllib.parse import urljoin

import requests
from requests.exceptions import ConnectionError

MAX_TRIES = 10
NGINX_URL = "http://nginx-server-tests"


def expect_status_code(
    url: str,
    expected_code: int,
):
    if url.startswith("/"):
        url = urljoin(NGINX_URL, url)

    for attempts in range(1, MAX_TRIES):
        try:
            result = requests.get(url, timeout=1, allow_redirects=False)
            break
        except ConnectionError:
            result = lambda x: None
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


def assert_status_ok(url: str):
    expect_status_code(url, 200)


def assert_status_ignored(url: str):
    expect_status_code(url, 444)


def assert_status_notfound(url: str):
    expect_status_code(url, 404)


def test_intended_endpoints_ok():
    assert_status_ok("/health-check/")
    assert_status_ok("/")
    assert_status_ok("/about/")
    assert_status_ok("/api/ping/")


def test_suspicious_extensions_ignored():
    assert_status_ignored("/somefile.exe")
    assert_status_ignored("/path/to/admin.log")


def test_unknown_subdomains_ignored():
    assert_status_ignored("http://prefix.nginx-server-tests/api/ping/")
    assert_status_ignored("http://sub.nginx-server-tests/")


def test_resource_extensions():
    assert_status_notfound("/static/file.js")
    assert_status_notfound("/media/file.js")

    assert_status_ignored("/static/file.exe")
