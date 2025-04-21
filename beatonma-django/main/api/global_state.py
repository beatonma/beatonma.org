from django.http import HttpRequest
from django.views.decorators.cache import cache_page
from main.models import MessageOfTheDay, SiteHCard
from ninja import Router, Schema
from ninja.decorators import decorate_view

router = Router()


class GlobalState(Schema):
    motd: str | None
    hcard: str | None


@router.get("/state/", response=GlobalState)
@decorate_view(cache_page(60 * 60))
def get_global_state(request: HttpRequest):
    hcard = SiteHCard.objects.singleton()
    hcard_html = hcard.html if hcard else None

    motd = MessageOfTheDay.objects.get_current()
    motd_html = motd.content_html if motd else None

    return {
        "motd": motd_html,
        "hcard": hcard_html,
    }
