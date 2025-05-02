import logging
from datetime import datetime

from common.schema import Mention
from django.http import HttpRequest
from django.shortcuts import redirect
from django.utils import timezone
from main.util import to_absolute_url
from mentions import config as mentions_config
from mentions.models import Webmention
from mentions.tasks import handle_outgoing_webmentions
from ninja import Form, Router, Schema
from pydantic import Field
from webmentions_tester.models import TemporaryMention

log = logging.getLogger(__name__)
router = Router(tags=["Webmentions tester"])


class TempMentionStatus(Schema):
    successful: bool
    status_code: int = Field(alias="response_code")
    message: str = Field(alias="status_message")
    source_url: str
    target_url: str
    endpoint: str | None = Field(alias="target_webmention_endpoint")


class TempMention(Schema):
    url: str
    submitted_at: datetime = Field(alias="submission_time")
    expires_at: datetime = Field(alias="expiration_time")
    status: TempMentionStatus | None = Field(alias="outgoing_status")


class WebmentionTesterSchema(Schema):
    temporary_outgoing_mentions: list[TempMention]
    mentions: list[Mention]


@router.get("/", response=WebmentionTesterSchema)
def get_temporary_webmentions(request: HttpRequest, url_path: str):
    if not url_path.startswith("/"):
        raise ValueError("url_path must be a relative URL path")

    url_without_schema = (
        mentions_config.build_url(url_path)
        .removeprefix("http://")  # remove schema
        .removeprefix("https://")  # remove schema
        .removesuffix("/")  # remove trailing slash
    )

    # Get mentions for url, allowing http/https and with/without a trailing slash.
    mentions = (
        Webmention.objects.filter_public()
        .filter(target_url__regex=rf"https?://{url_without_schema}/?")
        .distinct("source_url")
        .order_by("source_url", "-created_at")
    )
    temporary_mentions = TemporaryMention.objects.active(timezone.now())

    return {
        "temporary_outgoing_mentions": temporary_mentions,
        "mentions": mentions,
    }


@router.post("/")
def post_webmention(request: HttpRequest, url: Form[str]):
    TemporaryMention.objects.create(url=url)
    frontend_url = to_absolute_url("/webmentions_tester/")

    handle_outgoing_webmentions(
        frontend_url,
        f'<html><body><a href="{url}">{url}</a></body></html>',
    )

    return redirect(frontend_url)
