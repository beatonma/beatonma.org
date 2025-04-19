import json
from typing import Optional

from common.views.logged import LoggedView
from django.forms import fields, forms
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from mentions.models import OutgoingWebmentionStatus
from mentions.tasks import handle_outgoing_webmentions
from webmentions_tester import view_names
from webmentions_tester.models import (
    TemporaryMention,
    get_active_temporary_mentions,
    get_temp_webmention_ttl_seconds,
)


class WebmentionsTesterView(LoggedView):
    def get(self, request):
        now = timezone.now()
        active_mentions = get_active_temporary_mentions(now)

        return render(
            request,
            "webmentions_tester.html",
            {
                "active_mentions": {x.url for x in active_mentions},
            },
        )


class TempMentionForm(forms.Form):
    url = fields.URLField()


def _serialize_status(status: OutgoingWebmentionStatus) -> Optional[dict]:
    if status is None:
        return None

    return {
        "successful": status.successful,
        "status_code": status.response_code,
        "message": status.status_message,
        "source_url": status.source_url,
        "target_url": status.target_url,
        "endpoint": status.target_webmention_endpoint,
    }


class TemporaryMentionsView(View):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        now = timezone.now()
        active_mentions = get_active_temporary_mentions(now)
        ttl = get_temp_webmention_ttl_seconds()

        mentions = [
            {
                "url": m.url,
                "submitted_at": m.submission_time,
                "expires_at": m.expiration_time,
                "expires_in": (m.expiration_time - now).seconds,
                "status": _serialize_status(m.outgoing_status),
            }
            for m in active_mentions
        ]

        data = {
            "ttl": ttl,
            "mentions": mentions,
        }

        return JsonResponse(data)

    def post(self, request):
        data = json.loads(request.body)

        f = TempMentionForm(data)
        if f.is_valid():
            url = f.cleaned_data["url"]

            TemporaryMention.objects.create(url=url)
            self_url = reverse(view_names.WEBMENTIONS_TESTER)
            handle_outgoing_webmentions(
                self_url,
                f'<html><body><a href="{url}">{url}</a></body></html>',
            )

            return redirect(self_url)

        else:
            return HttpResponseBadRequest(f"Url validation failed {data}")
