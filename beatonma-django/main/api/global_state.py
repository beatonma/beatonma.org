from django.http import HttpRequest
from main.models import MessageOfTheDay, SiteHCard
from ninja import Router, Schema

router = Router()


class GlobalState(Schema):
    motd: str | None
    hcard: str | None


@router.get("/state/", response=GlobalState)
def get_global_state(request: HttpRequest):
    hcard = SiteHCard.objects.singleton()
    hcard_html = hcard.html if hcard else None

    motd = MessageOfTheDay.objects.get_current()
    motd_html = motd.content_html if motd else None

    return {
        "motd": motd_html,
        "hcard": hcard_html,
    }
