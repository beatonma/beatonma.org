import logging
from datetime import datetime
from typing import List
from uuid import UUID

from bma_app.api.schemas import NoteSchema
from bma_app.api.util import no_null_dict
from common.models.generic import generic_fk
from django.http import HttpRequest, HttpResponse
from main.models import Note, RelatedFile
from ninja import File, Form, Router, Schema, UploadedFile
from ninja.pagination import paginate

log = logging.getLogger(__name__)
router = Router()


class UploadFileSchema(Schema):
    file_description: str = None


class CreateNoteSchema(Schema):
    published_at: datetime = None
    content: str
    is_published: bool
    file_description: str = None


class CreatedResponseSchema(Schema):
    id: UUID


class EditNoteSchema(Schema):
    content: str | None = None
    is_published: bool
    published_at: datetime | None = None


@router.get("/", response=List[NoteSchema], url_name="get-notes")
@paginate
def get_notes(request):
    return Note.objects.sort_by_recent()


@router.post("/", response={201: CreatedResponseSchema})
def create_note(
    request: HttpRequest,
    response: HttpResponse,
    form: Form[CreateNoteSchema],
    file: File[UploadedFile] = None,
):
    note_kwargs = no_null_dict(
        content=form.content,
        is_published=form.is_published,
        published_at=form.published_at,
    )
    note = Note.objects.create(**note_kwargs)

    if file:
        _create_related_file(note, form.file_description, file)

    response.headers["Location"] = note.get_absolute_url()
    return {"id": note.api_id}


@router.post(
    "/{uuid}/media/",
    response={201: CreatedResponseSchema},
    url_name="add-media-to-note",
)
def upload_media(
    request: HttpRequest,
    uuid: UUID,
    form: Form[UploadFileSchema],
    file: File[UploadedFile],
):
    note = Note.objects.get(api_id=uuid)
    file = _create_related_file(note, form.file_description, file)

    return {"id": file.api_id}


@router.get("/{uuid}/", response=NoteSchema, url_name="get-note")
def get_note(request: HttpRequest, uuid: UUID):
    return Note.objects.get(api_id=uuid)


@router.patch("/{uuid}/", response=NoteSchema, url_name="update-note")
def update_note(request: HttpRequest, uuid: UUID, changes: EditNoteSchema):
    note = Note.objects.get(api_id=uuid).update(
        **no_null_dict(
            content=changes.content,
            is_published=changes.is_published,
            published_at=changes.published_at,
        ),
    )
    return note


@router.delete("/{uuid}/", response={204: None}, url_name="delete-note")
def delete_note(request: HttpRequest, uuid: UUID):
    Note.objects.get(api_id=uuid).delete()
    return 204, None


def _create_related_file(
    note: Note,
    file_description: str | None,
    file: File[UploadedFile],
):
    return RelatedFile.objects.create(
        file=file,
        description=file_description,
        **generic_fk(note),
    )
