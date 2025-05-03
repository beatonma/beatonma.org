from datetime import date

from django.http import HttpRequest
from django.views.decorators.cache import cache_page
from main.models import MessageOfTheDay, PointsOfInterest, SiteHCard
from main.models.mixins.cache import GlobalStateCacheMixin
from ninja import Router, Schema
from ninja.decorators import decorate_view
from pydantic import Field

from .schema import File, Link

router = Router()


class HAdr(Schema):
    locality: str | None
    region: str | None
    country: str | None


class GlobalHCard(Schema):
    name: str
    url: str
    photo: File | None
    logo: File | None
    location: HAdr | None
    birthday: date | None
    relme: list[Link] = Field(alias="links")

    @staticmethod
    def resolve_location(obj):
        return {
            "locality": obj.locality,
            "region": obj.region,
            "country": obj.country,
        }


class GlobalState(Schema):
    motd: str | None
    hcard: GlobalHCard | None
    poi: list[Link]


@router.get("/state/", response=GlobalState)
@decorate_view(cache_page(60 * 60, key_prefix=GlobalStateCacheMixin.cache_key))
def get_global_state(request: HttpRequest):
    hcard = SiteHCard.objects.singleton()

    poi = PointsOfInterest.objects.singleton()
    poi_links = poi.links if poi else []

    motd = MessageOfTheDay.objects.get_current()
    motd_html = motd.content_html if motd else None

    return {
        "motd": motd_html,
        "hcard": hcard,
        "poi": poi_links,
    }
