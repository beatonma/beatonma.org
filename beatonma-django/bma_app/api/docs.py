from django.http import HttpRequest
from ninja import Router
from ninja.openapi.views import openapi_json, openapi_view

router = Router()


@router.get("/", include_in_schema=False)
def docs(request: HttpRequest):
    return openapi_view(request, router.api)


@router.get("/openapi.json", url_name="openapi-json", include_in_schema=False)
def json(request: HttpRequest):
    return openapi_json(request, router.api)
