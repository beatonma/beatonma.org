import logging
from typing import Optional

from common.util import http
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.pagination import RouterPaginated
from ninja.security.apikey import APIKeyBase

from .. import auth
from .docs import router as docs_router
from .media import router as media_router
from .notes import router as notes_router

log = logging.getLogger(__name__)


class TokenAuth(APIKeyBase):
    param_name = "token"

    def _get_key(self, request: HttpRequest) -> Optional[str]:
        return auth.get_token(request)

    def authenticate(self, request: HttpRequest, key: str):
        try:
            return auth.check_token(key)
        except auth.BadApiToken:
            raise
        except auth.ApiTokenException:
            if request.user.is_staff:
                return request.user
            raise


api = NinjaAPI(
    docs_url=None,
    openapi_url=None,
    urls_namespace="ninja-api",
    title="API",
    version="2.0",
    default_router=RouterPaginated(),
    auth=TokenAuth(),
)
api.add_router("/", docs_router)
api.add_router("/notes/", notes_router)
api.add_router("/media/", media_router)


@api.exception_handler(auth.ApiTokenException)
def on_bad_token(request, exception):
    return api.create_response(
        request,
        {"detail": "Bad user or auth key."},
        status=http.STATUS_401_UNAUTHORIZED,
    )


@api.exception_handler(Exception)
def on_bad_token(request, exception):
    return api.create_response(
        request,
        {"detail": f"{exception}"},
        status=http.STATUS_400_BAD_REQUEST,
    )
