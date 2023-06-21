import logging
import math
import os
import time
from typing import Dict, Iterable, List

from common.models import PageView
from contact.models.webmailmessage import WebmailMessage
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.views import View
from github.models import GithubEventUpdateCycle
from mentions.models import SimpleMention, Webmention
from mentions.models.mixins import QuotableMixin
from mentions.views.serialize import serialize_hcard

log = logging.getLogger(__name__)


class StaffView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseNotFound()
        else:
            return super().dispatch(request, *args, **kwargs)


class DashboardView(StaffView):
    def get(self, request, *args, **kwargs):
        return render(request, "dashboard.html")


class DashboardApiView(StaffView):
    def get(self, request, *args, **kwargs):
        webmentions = Webmention.objects.all()[:10]
        simple_mentions = SimpleMention.objects.all()[:10]
        mentions = list(webmentions) + list(simple_mentions)

        pageviews = [view.to_json() for view in PageView.objects.all()[:25]]
        webmail = [mail.to_json() for mail in WebmailMessage.objects.all()[:10]]

        github = {
            "cached_at": GithubEventUpdateCycle.objects.first().created_at,
        }

        system = {
            "uptime": _get_system_uptime(),
        }

        return JsonResponse(
            {
                "system": system,
                "github": github,
                "mentions": _serialize_mentions(mentions),
                "views": pageviews,
                "webmail": webmail,
            }
        )


def _get_system_uptime():
    uptime_seconds = int(time.clock_gettime(time.CLOCK_BOOTTIME))
    hours = math.floor(uptime_seconds / 3600)
    seconds = uptime_seconds - (hours * 3600)
    minutes = math.floor(seconds / 60)
    seconds = math.floor(seconds - (minutes * 60))
    if hours:
        return f"{hours}h {minutes}m {seconds}s"
    else:
        return f"{minutes}m {seconds}s"


def _get_system_ram_percentage():
    total_ram, used_ram, free_ram = map(
        int, os.popen("free -t -m").readlines()[-1].split()[1:]
    )
    return int(used_ram / total_ram * 100)


def _serialize_mentions(mentions: Iterable[QuotableMixin]) -> List[Dict]:
    def _typeof(mention) -> str:
        if isinstance(mention, Webmention):
            return "webmention"
        elif isinstance(mention, SimpleMention):
            return "simple"
        else:
            raise ValueError(f"Unhandled mention type: {mention}")

    return [
        {
            "hcard": serialize_hcard(mention.hcard),
            "quote": mention.quote,
            "source_url": mention.source_url,
            "target_url": mention.target_url,
            "published": mention.published,
            "type": _typeof(mention),
        }
        for mention in mentions
    ]
