import logging

from contact.tasks import send_webmail
from contact.tasks.recaptcha import UnverifiedRecaptcha, verify_recaptcha
from django.http import HttpRequest
from ninja import Field, Router, Schema

router = Router(tags=["Contact"])

log = logging.getLogger(__name__)


class ContactForm(Schema):
    name: str = Field(min_length=2, max_length=48)
    contact_info: str = Field(min_length=2, max_length=256)
    message: str = Field(min_length=2, max_length=2048)
    recaptcha_token: str


@router.post("/", response={204: None, 400: None})
def send_mail(request: HttpRequest, form: ContactForm):
    log.info(request, form)

    try:
        verify_recaptcha(form.recaptcha_token)
        send_webmail.delay(
            name=form.name,
            contact_info=form.contact_info,
            message=form.message,
        )
        return 204, None
    except UnverifiedRecaptcha as e:
        log.error(f"Recaptcha verification failed: {e}")
        return 400, None
