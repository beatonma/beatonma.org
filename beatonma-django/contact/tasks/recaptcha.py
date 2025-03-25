import logging
from datetime import datetime

import requests
from django.conf import settings
from pydantic import BaseModel as Schema

log = logging.getLogger(__name__)


class Response(Schema):
    success: bool
    challenge_ts: datetime
    hostname: str
    error_codes: list[str] | None = None


class UnverifiedRecaptcha(Exception):
    """Raised when a recaptcha token fails verification with the Recaptcha service."""

    pass


def verify_recaptcha(token: str):
    data = {
        "response": token,
        "secret": settings.GOOGLE_RECAPTCHA_SECRET,
    }

    r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
    response = Response.model_validate(r.json())

    if response.success:
        log.info(f"Recaptcha verified")
        return

    raise UnverifiedRecaptcha(",".join(response.error_codes or []))
