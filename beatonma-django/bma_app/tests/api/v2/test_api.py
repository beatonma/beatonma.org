import json

from basetest.testcase import LocalTestCase
from bma_app import auth
from bma_app.api import api
from bma_app.models import ApiToken
from common.util import http
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse


class ApiTestCase(LocalTestCase):
    def setUp(self):
        super().setUp()
        self.staff_user = User.objects.create_user(
            username="test-user",
            is_staff=True,
        )
        self.token = ApiToken.objects.create(
            user=self.staff_user, enabled=True
        ).uuid.hex
        self.token_disabled = ApiToken.objects.create(user=self.staff_user).uuid.hex

    def get_with_api_token(
        self, url: str, data=None, headers: dict | None = None, **kwargs
    ):
        return self._client_method_with_api_token(
            self.client.get, url, data, headers, **kwargs
        )

    def post_with_api_token(
        self, url: str, data=None, headers: dict | None = None, **kwargs
    ):
        return self._client_method_with_api_token(
            self.client.post, url, data, headers, **kwargs
        )

    def patch_with_api_token(
        self, url: str, data: dict, headers: dict | None = None, **kwargs
    ):
        return self._client_method_with_api_token(
            self.client.patch,
            url,
            json.dumps(data),
            headers,
            content_type="application/json",
            **kwargs,
        )

    def delete_with_api_token(
        self, url: str, data=None, headers: dict | None = None, **kwargs
    ):
        return self._client_method_with_api_token(
            self.client.delete, url, data, headers, **kwargs
        )

    def _client_method_with_api_token(
        self, method, url: str, data=None, headers: dict = None, **kwargs
    ) -> HttpResponse:
        if not headers:
            headers = {}
        headers[auth.HEADER_TOKEN] = self.token

        return method(url, data=data, headers=headers, **kwargs)


class ApiRootPermissionsTests(ApiTestCase):
    view_name = f"{api.urls_namespace}:api-root"

    def _get(self, token, headers=None):
        data = {auth.TOKEN_KEY: token} if token else None
        return self.client.get(reverse(self.view_name), data=data, headers=headers)

    def test_root_accessible_to_staff(self):
        self.client.force_login(self.staff_user)
        response = self._get(token=None)
        self.assertEqual(response.status_code, http.STATUS_200_OK)

    def test_root_inaccessible_to_anon(self):
        response = self._get(token=None)
        self.assertEqual(response.status_code, http.STATUS_401_UNAUTHORIZED)

    def test_root_accessible_to_anon_with_token(self):
        response = self._get(token=self.token)
        self.assertEqual(response.status_code, http.STATUS_200_OK)

    def test_root_inaccessible_to_staff_with_wrong_token(self):
        """Staff should be able to access with or without a token, but trying to use a bad token be a problem."""
        response = self._get(token=self.token_disabled)
        self.assertEqual(response.status_code, http.STATUS_401_UNAUTHORIZED)

    def test_root_inaccessible_to_anon_with_wrong_token(self):
        response = self._get(token=self.token_disabled)
        self.assertEqual(response.status_code, http.STATUS_401_UNAUTHORIZED)

        response = self._get(token="whatever")
        self.assertEqual(response.status_code, http.STATUS_401_UNAUTHORIZED)

    def test_root_accessible_with_key_in_headers(self):
        response = self._get(token=None, headers={auth.HEADER_TOKEN: self.token})
        self.assertEqual(response.status_code, http.STATUS_200_OK)
