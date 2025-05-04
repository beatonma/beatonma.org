import logging
from datetime import datetime
from typing import Annotated
from uuid import UUID

from bma_app.api.pagination import OffsetPagination
from bma_app.api.schemas import PostSchema
from bma_app.api.util import no_null_dict
from common.models.generic import generic_fk
from common.util.time import coerce_tzdatetime
from django.http import HttpRequest, HttpResponse
from main.models import Post, RelatedFile
from ninja import File, Form, Router, Schema, UploadedFile
from ninja.pagination import paginate
from pydantic import AfterValidator

log = logging.getLogger(__name__)
router = Router()


def _tz(dt):
    return coerce_tzdatetime(dt)


TimezoneAwareDatetime = Annotated[datetime | None, AfterValidator(_tz)]


class UploadFileSchema(Schema):
    file_description: str = None


class CreatePostSchema(Schema):
    published_at: TimezoneAwareDatetime = None
    content: str
    is_published: bool
    file_description: str = None


class CreatedResponseSchema(Schema):
    id: UUID


class EditPostSchema(Schema):
    content: str | None = None
    is_published: bool
    published_at: TimezoneAwareDatetime = None


@router.get("/", response=list[PostSchema])
@paginate(OffsetPagination)
def get_posts(request):
    return Post.objects.sort_by_recent()


@router.post("/", response={201: CreatedResponseSchema})
def create_post(
    request: HttpRequest,
    response: HttpResponse,
    form: Form[CreatePostSchema],
    file: File[UploadedFile] = None,
):
    post_kwargs = no_null_dict(
        content=form.content,
        is_published=form.is_published,
        published_at=form.published_at,
    )
    post = Post.objects.create(**post_kwargs)

    if file:
        _create_related_file(post, form.file_description, file)

    response.headers["Location"] = post.get_absolute_url()
    return {"id": post.api_id}


@router.post(
    "/{uuid}/media/",
    response={201: CreatedResponseSchema},
)
def add_media_to_post(
    request: HttpRequest,
    uuid: UUID,
    form: Form[UploadFileSchema],
    file: File[UploadedFile],
):
    post = Post.objects.get(api_id=uuid)
    file = _create_related_file(post, form.file_description, file)

    return {"id": file.api_id}


@router.get("/{uuid}/", response=PostSchema)
def get_post(request: HttpRequest, uuid: UUID):
    return Post.objects.get(api_id=uuid)


@router.patch("/{uuid}/", response=PostSchema)
def update_post(request: HttpRequest, uuid: UUID, changes: EditPostSchema):
    post = Post.objects.get(api_id=uuid).update(
        **no_null_dict(
            content=changes.content,
            is_published=changes.is_published,
            published_at=changes.published_at,
        ),
    )
    return post


@router.delete("/{uuid}/", response={204: None})
def delete_post(request: HttpRequest, uuid: UUID):
    Post.objects.get(api_id=uuid).delete()
    return 204, None


def _create_related_file(
    post: Post,
    file_description: str | None,
    file: File[UploadedFile],
):
    return RelatedFile.objects.create(
        file=file,
        description=file_description,
        **generic_fk(post),
    )
