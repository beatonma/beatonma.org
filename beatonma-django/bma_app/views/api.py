import logging

from bma_app.models import ApiToken
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from rest_framework.permissions import BasePermission
from rest_framework.viewsets import ModelViewSet

log = logging.getLogger(__name__)


HEADER_TOKEN = "ApiToken"
TOKEN_KEY = "token"


class ApiTokenException(Exception):
    pass


class BadApiToken(ApiTokenException):
    pass


class ApiTokenPermission(BasePermission):
    def has_permission(self, request, view):
        return has_api_permission(request)

    def has_object_permission(self, request, view, obj):
        return has_api_permission(request)


class ApiViewSet(ModelViewSet):
    permission_classes = (ApiTokenPermission,)


def has_api_permission(request: HttpRequest) -> bool:
    token = (
        request.headers.get(HEADER_TOKEN)
        or request.GET.get(TOKEN_KEY)
        or request.POST.get(TOKEN_KEY)
    )

    try:
        check_token(token)
        return True
    except BadApiToken:
        return False
    except ApiTokenException:
        if request.user.is_staff:
            return True

    return False


def check_token(user_token: str) -> None:
    """Raises ApiTokenException if user_token does not map to a valid staff user."""
    if not user_token:
        log.warning("Missing API token.")
        raise ApiTokenException()

    try:
        token = ApiToken.objects.filter(uuid=user_token).first()
    except ValidationError:
        log.warning(f"Unknown API token: {user_token}")
        raise BadApiToken()

    if token is None or not token.enabled:
        log.warning(f"Bad API token: {token}")
        raise BadApiToken()

    if not token.user.is_staff:
        log.warning(f"Bad API token user: {token.user}")
        raise BadApiToken()
