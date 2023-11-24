import logging
from typing import Optional

from bma_app.models import ApiToken
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

log = logging.getLogger(__name__)


TOKEN_KEY = "token"


class ApiTokenException(Exception):
    pass


class ApiViewSet(ModelViewSet):
    def dispatch(self, request: Request, *args, **kwargs):
        print(request.META)
        return check_request_token(request) or super().dispatch(
            request, *args, **kwargs
        )


def check_request_token(request: Request) -> Optional[HttpResponse]:
    """Return None if the request passes validation, else return HTTP 403.

    Valid requests:
    - The signed-in user is a staff member, or
    - The request includes a valid API token which corresponds to a staff user.
    """
    method = request.method.upper()
    if method == "GET":
        try:
            check_token(request.GET.get(TOKEN_KEY))
        except ApiTokenException:
            # If token validation fails, allow access only if user is staff.
            if not request.user.is_staff:
                return HttpResponse(status=403)
        return

    if method == "POST":
        try:
            check_token(request.POST.get(TOKEN_KEY))
            return
        except ApiTokenException:
            return HttpResponse(status=403)

    raise ApiTokenException(f"Unhandled method '{method}'")


def check_token(user_token: str):
    """Raises ApiTokenException if user_token does not map to a valid staff user."""
    if not user_token:
        log.warning("Missing API token.")
        raise ApiTokenException()

    try:
        token = ApiToken.objects.filter(uuid=user_token).first()
    except ValidationError:
        log.warning(f"Unknown API token: {user_token}")
        raise ApiTokenException()

    if token is None or not token.enabled:
        log.warning(f"Bad API token: {token}")
        raise ApiTokenException()

    if not token.user.is_staff:
        log.warning(f"Bad API token user: {token.user}")
        raise ApiTokenException()
