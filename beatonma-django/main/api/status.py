from common.util.client import get_client_ip
from django.http import HttpRequest
from django_user_agents.utils import get_user_agent
from ninja import Router, Schema
from pydantic import IPvAnyAddress

router = Router()


@router.get("/ping/")
def ping(request: HttpRequest):
    return 200, "OK"


@router.api_operation(["HEAD"], "/ping/", response={204: None})
def ping(request: HttpRequest):
    return 204, None


class WhoAmiISchema(Schema):
    ip: IPvAnyAddress
    device: str
    os: str
    browser: str


@router.get("/whoami/", response=WhoAmiISchema)
def whoami(request: HttpRequest):
    ip = get_client_ip(request)
    ua = get_user_agent(request)

    return {
        "ip": ip,
        "device": ua.get_device(),
        "os": ua.get_os(),
        "browser": ua.get_browser(),
    }
