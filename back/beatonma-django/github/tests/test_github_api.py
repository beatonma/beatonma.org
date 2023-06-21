import datetime
from unittest.mock import patch

import requests
from basetest.testcase import LocalTestCase, NetworkTestCase
from github import github_api
from github.models import GithubETag

ETAG = 'W/"3aaaa33aaaa3a333333a33a3aaaaaa3a3333a333a3a33a333aa3aaa33333333a"'

SAMPLE_RESPONSE_HEADERS = {
    "Server": "GitHub.com",
    "Date": "Sun, 03 Apr 2022 09:57:01 GMT",
    "Content-Type": "application/json; charset=utf-8",
    "Transfer-Encoding": "chunked",
    "Cache-Control": "private, max-age=60, s-maxage=60",
    "Vary": "Accept, Authorization, Cookie, X-GitHub-OTP, Accept-Encoding, Accept, X-Requested-With",
    "ETag": ETAG,
    "X-OAuth-Scopes": "repo, workflow",
    "X-Accepted-OAuth-Scopes": "",
    "X-GitHub-Media-Type": "github.v3; format=json",
    "Link": '<https://api.github.com/user/repos?sort=updated&page=2>; rel="next", <https://api.github.com/user/repos?sort=updated&page=2>; rel="last"',
    "X-RateLimit-Limit": "5000",
    "X-RateLimit-Remaining": "4967",
    "X-RateLimit-Reset": "3333333333",
    "X-RateLimit-Used": "33",
    "X-RateLimit-Resource": "core",
    "Access-Control-Expose-Headers": "ETag, Link, Location, Retry-After, X-GitHub-OTP, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Used, X-RateLimit-Resource, X-RateLimit-Reset, X-OAuth-Scopes, X-Accepted-OAuth-Scopes, X-Poll-Interval, X-GitHub-Media-Type, X-GitHub-SSO, X-GitHub-Request-Id, Deprecation, Sunset",
    "Access-Control-Allow-Origin": "*",
    "Strict-Transport-Security": "max-age=31536000; includeSubdomains; preload",
    "X-Frame-Options": "deny",
    "X-Content-Type-Options": "nosniff",
    "X-XSS-Protection": "0",
    "Referrer-Policy": "origin-when-cross-origin, strict-origin-when-cross-origin",
    "Content-Security-Policy": "default-src 'none'",
    "Content-Encoding": "gzip",
    "X-GitHub-Request-Id": "A333:AA33:333333A:333AA33:33333AAA",
}

URL = "https://api.not-github.com/my-fake-url/"


class _MockResponse:
    def __init__(self, req: requests.PreparedRequest):
        self.headers = dict(**SAMPLE_RESPONSE_HEADERS)

        if req.headers.get("If-None-Match") == ETAG:
            self.status_code = 304

        else:
            self.status_code = 200


class GithubApiTest(LocalTestCase):
    def test_parse_response_headers(self):
        headers = SAMPLE_RESPONSE_HEADERS

        parsed = github_api._parse_response_headers(headers)

        self.assertEqual(
            parsed.etag,
            ETAG,
        )
        self.assertEqual(
            parsed.timestamp,
            datetime.datetime(2022, 4, 3, 9, 57, 1, tzinfo=datetime.timezone.utc),
        )

    def test_get_if_changed(self):
        with patch.object(
            github_api,
            "_get",
            side_effect=lambda req: _MockResponse(req),
        ):
            # No pre-existing ETag -> no previous content -> response OK
            response = github_api.get_if_changed(URL)
            self.assertEqual(response.status_code, 200)

            # ETag matches previous request-> content unchanged -> response 304 Not Modified -> return None
            response = github_api.get_if_changed(URL)
            self.assertIsNone(response)

            # Change our etag to simulate a change in response etag
            GithubETag.objects.update(
                etag="some-old-etag",
            )
            # ETag no longer matches -> content has changed -> response OK
            response = github_api.get_if_changed(URL)
            self.assertEqual(response.status_code, 200)

    def tearDown(self) -> None:
        self.teardown_models(
            GithubETag,
        )


class GithubApiTestActual(NetworkTestCase):
    def test_foreach(self):
        items_seen = 0
        names = []

        def _for_obj(obj):
            nonlocal items_seen, names
            items_seen += 1
            names.append(obj.get("full_name"))

        github_api.for_each("https://api.github.com/user/repos?sort=updated", _for_obj)

        print(names)
        self.assertEqual(items_seen, 41)
        raise Exception("Just checking...")

    def tearDown(self) -> None:
        self.teardown_models(
            GithubETag,
        )
