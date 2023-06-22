from dataclasses import dataclass
from typing import List, Optional

from common.models import ApiModel
from common.views.api import ApiView
from django.http import JsonResponse
from main.models import Note, RelatedFile
from main.views.querysets import get_notes


class ApiNotesView(ApiView):
    def get(self, request):
        notes_with_media = get_notes_with_media()

        return JsonResponse(
            {
                "notes": [note.to_json() for note in notes_with_media],
            },
        )


@dataclass
class NoteWithMedia(ApiModel):
    note: Note
    media: Optional[RelatedFile] = None

    def __post_init__(self):
        if not self.media:
            self.media = self.note.related_files.first()

    def to_json(self) -> dict:
        return dict(
            note=self.note.to_json(),
            media=self.media.to_json() if self.media else None,
        )


def get_notes_with_media(**filter_kwargs) -> List[NoteWithMedia]:
    return [NoteWithMedia(note) for note in get_notes(**filter_kwargs)]
