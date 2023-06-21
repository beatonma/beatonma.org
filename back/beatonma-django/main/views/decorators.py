import logging
from functools import wraps

import requests
from django.conf import settings
from django.http import HttpResponseBadRequest, QueryDict

from common.views.api import ApiView

log = logging.getLogger(__name__)


RECAPTCHA_KEY = "g-recaptcha-response"


class UnverifiedRecaptcha(Exception):
    """Raised when a recaptcha token fails verification with the Recaptcha service."""

    pass


def recaptcha(f):
    """
    Decorator to verify Recaptcha tokens.
    Raises UnverifiedRecaptcha if verification fails.
    """

    @wraps(f)
    def verify_recaptcha(http_post: QueryDict, *args, **kwargs):
        token = http_post.get(RECAPTCHA_KEY)
        if not token:
            raise ValueError("Recaptcha token is missing")

        data = {
            "response": token,
            "secret": settings.GOOGLE_RECAPTCHA_SECRET,
        }

        r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)

        j = r.json()
        if j.get("success") is True:
            log.info(f"Recaptcha verified: {j}")
            f(http_post, *args, **kwargs)

        else:
            log.warning(f"Recaptcha failed verification: {j}")
            raise UnverifiedRecaptcha(f"{j}")

    return verify_recaptcha


class RecaptchaView(ApiView):
    """A View that ensures a recaptcha token is present in POST requests.

    The token is not verified! The view only checks that the RECAPTCHA_KEY field
    exists in POST parameters. The actual verification must be done using a
    function decorated with @recaptcha.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            token = request.POST.get(RECAPTCHA_KEY)
            if not token:
                return HttpResponseBadRequest("Recaptcha token required")

        return super().dispatch(request, *args, **kwargs)
