import re
import uuid

from bma_app.tests.test_drf import DrfTestCase
from bma_app.views.api import TOKEN_KEY
from common.models.generic import generic_fk
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.urls import reverse
from main.models import Note, RelatedFile
from rest_framework import status


class NoteGetTests(DrfTestCase):
    def test_note_structure_is_correct(self):
        note = Note.objects.create(content="This is content")
        file = RelatedFile.objects.create(
            file=_file(), description="file description", **generic_fk(note)
        )

        response = self.get_with_api_token(reverse("api:note-list"))
        data = response.json()[0]

        match data:
            case {
                "id": str(),
                "content_html": str(),
                "url": str(),
                "timestamp": str(),
                "is_published": bool(),
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


class DrfCreateNoteTests(DrfTestCase):
    def post_request(
        self,
        content: str = None,
        token: str | bool | None = True,
        file: File | None = None,
        file_description: str | None = None,
        is_published: bool = True,
        note_id: str | None = None,
    ) -> HttpResponse:
        data = {
            TOKEN_KEY: self.token if token is True else token,
            "id": note_id,
            "content": content,
            "file": file,
            "file_description": file_description,
            "is_published": is_published,
        }

        empty_keys = [key for key in data.keys() if data[key] is None]
        for key in empty_keys:
            del data[key]
        return self.client.post(reverse("api:note-list"), data)

    def test_missing_usertoken_returns_403(self):
        response = self.post_request(content="missing token", token=None)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_usertoken_returns_403(self):
        response = self.post_request(content="wrong token", token=uuid.uuid4().hex)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_simple_note(self):
        response = self.post_request(content="drf test")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(Note.objects.get(content="drf test"))

    def test_create_note_with_media(self):
        response = self.post_request(
            content="drf note with media",
            file=_file(),
            file_description="Drf description",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        note = Note.objects.get(content="drf note with media")
        file: RelatedFile = note.related_files.first()

        self.assertRegex(str(file.file), r"related/\d{4}/[-\w]+\.\w+$")
        self.assertEqual(file.description, "Drf description")

    def test_edit_note(self):
        note = Note.objects.create(content="unedited note :(", is_published=False)
        response = self.put_with_api_token(
            reverse("api:note-detail", args=[note.api_id]),
            {
                "content": "edited note :)",
                "is_published": True,
            },
        )
        note.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(note.content, "edited note :)")
        self.assertTrue(note.is_published)

    def test_delete_note(self):
        note = Note.objects.create(content="delete this")
        response = self.delete_with_api_token(
            reverse("api:note-detail", args=[note.api_id])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Note.DoesNotExist):
            note.refresh_from_db()


class DrfNoteMediaTests(DrfTestCase):
    def test_append_media_to_existing_note(self):
        note = Note.objects.create(content="Hello")

        response = self.client.post(
            reverse("api:note-media", args=[note.api_id]),
            dict(
                token=self.token,
                file=_file(),
                file_description="Added later",
            ),
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        file: RelatedFile = note.related_files.first()

        self.assertEqual(file.description, "Added later")

    def test_delete_media(self):
        note = Note.objects.create(content="delete the media")
        file = RelatedFile.objects.create(file=_file(), **generic_fk(note))

        response = self.delete_with_api_token(
            reverse("api:relatedfile-detail", args=[file.api_id]),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(RelatedFile.DoesNotExist):
            file.refresh_from_db()

    def test_update_media(self):
        note = Note.objects.create(content="delete the media")
        file = RelatedFile.objects.create(
            file=_file(), description="unedited", **generic_fk(note)
        )

        response = self.put_with_api_token(
            reverse("api:relatedfile-detail", args=[file.api_id]),
            {
                "description": "edited!",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        file.refresh_from_db()
        self.assertEqual(file.description, "edited!")


def _file():
    return SimpleUploadedFile(
        "file.txt",
        b"__FILE_CONTENTS__",
        content_type="multipart/form-data",
    )
