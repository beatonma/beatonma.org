import re

from bma_app.tests.api.v2.test_api import ApiTestCase
from common.models.generic import generic_fk
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from main.models import Note, RelatedFile


class NoteGetTests(ApiTestCase):
    def test_note_structure_is_correct(self):
        note = Note.objects.create(content="This is content")
        file = RelatedFile.objects.create(
            file=_file(), description="file description", **generic_fk(note)
        )

        response = self.get_with_api_token(reverse("ninja-api:get-notes"))
        data = response.json()["results"][0]

        match data:
            case {
                "id": str(),
                "content": str(),
                "content_html": str(),
                "url": str(),
                "is_published": bool(),
                "published_at": str(),
                "media": [
                    {
                        "id": str(),
                        "url": str(),
                        "description": str(),
                        "type": str(),
                    }
                ],
            }:
                pass
            case _:
                raise AssertionError(f"Unexpected data structure: {data}")

        # Ensure that ID fields are using UUIDs, not default integer PK.
        uuid_pattern = re.compile(r"(?=.*[a-zA-Z])(?=.*[0-9])[\-a-zA-Z0-9]+")
        self.assertRegex(data["id"], uuid_pattern)
        self.assertEqual(data["id"], str(note.api_id))

        self.assertRegex(data["media"][0]["id"], uuid_pattern)
        self.assertEqual(data["media"][0]["id"], str(file.api_id))


def _file():
    return SimpleUploadedFile(
        "file.txt",
        b"__FILE_CONTENTS__",
        content_type="multipart/form-data",
    )
