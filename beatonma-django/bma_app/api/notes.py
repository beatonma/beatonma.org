import logging
from datetime import datetime
from typing import List
from uuid import UUID

from bma_app.api.schemas import NoteSchema
from common.models.generic import generic_fk
from django.http import HttpResponse
from main.models import Note, RelatedFile
from ninja import File, Form, Router, Schema, UploadedFile
from ninja.pagination import paginate

log = logging.getLogger(__name__)
router = Router()


class CreatedSchema(Schema):
    id: UUID


class CreateNoteSchema(Schema):
    published_at: datetime = None
    content: str
    is_published: bool
    file_description: str = None


@router.get("/", response=List[NoteSchema], url_name="get-notes")
@paginate
def get_notes(request):
    return Note.objects.sort_by_recent()


@router.post("/", response={201: CreatedSchema})
def create_note(
    request,
    response: HttpResponse,
    form: Form[CreateNoteSchema],
    file: File[UploadedFile],
):
    note_kwargs = {
        "content": form.content,
        "is_published": form.is_published,
        "published_at": form.published_at,
    }
    note_kwargs = {
        key: value for key, value in note_kwargs.items() if value is not None
    }
    note = Note.objects.create(**note_kwargs)

    if file:
        _create_related_file(note, form.file_description, file)

    response.headers["Location"] = note.get_absolute_url()
    return {"id": note.api_id}


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
