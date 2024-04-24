import logging

from bma_app.models import ApiToken
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.http import HttpRequest

log = logging.getLogger(__name__)

HEADER_TOKEN = "ApiToken"
TOKEN_KEY = "token"


class ApiTokenException(Exception):
    pass


class BadApiToken(ApiTokenException):
    pass


def get_token(request: HttpRequest) -> str | None:
    return (
        request.headers.get(HEADER_TOKEN)
        or request.GET.get(TOKEN_KEY)
        or request.POST.get(TOKEN_KEY)
    )


def has_api_permission(request: HttpRequest) -> bool:
    token = get_token(request)

    try:
        check_token(token)
        return True
    except BadApiToken:
        return False
    except ApiTokenException:
        if request.user.is_staff:
            return True

    log.warning(f"Missing API token for {request.get_full_path()}.")
    return False


def check_token(user_token: str) -> AbstractUser:
    """Raises ApiTokenException if user_token does not map to a valid staff user."""
    if not user_token:
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

    return token.user
