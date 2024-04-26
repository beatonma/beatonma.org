import logging
from uuid import UUID

from bma_app.api.schemas import MediaSchema
from common.util import http
from django.http import HttpRequest
from main.models import RelatedFile
from ninja import Router, Schema

log = logging.getLogger(__name__)
router = Router()


@router.get("/{uuid}/", response=MediaSchema, url_name="get-media")
def get_media(request: HttpRequest, uuid: UUID):
    return RelatedFile.objects.get(api_id=uuid)


class EditMediaSchema(Schema):
    description: str


@router.patch("/{uuid}/", response=MediaSchema, url_name="update-media")
def update_media(request: HttpRequest, uuid: UUID, changes: EditMediaSchema):
    file = RelatedFile.objects.get(api_id=uuid)
    file.update(description=changes.description)
    return file


@router.delete("/{uuid}/", response={204: None}, url_name="delete-media")
def delete_media(request: HttpRequest, uuid: UUID):
    RelatedFile.objects.get(api_id=uuid).delete()
    return http.STATUS_204_NO_CONTENT, None
