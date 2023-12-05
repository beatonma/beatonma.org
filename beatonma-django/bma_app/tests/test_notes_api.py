import uuid

from bma_app.tests.test_drf import DrfTestCase
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.urls import reverse
from main.models import Note, RelatedFile
from rest_framework import status


class DrfCreateNoteTests(DrfTestCase):
    def post_request(
        self,
        note: str = None,
        token: str | bool | None = True,
        file: File | None = None,
        file_description: str | None = None,
        is_published: bool = True,
        note_id: str | None = None,
    ) -> HttpResponse:
        data = {
            "token": self.token if token is True else token,
            "id": note_id,
            "content": note,
            "file": file,
            "file_description": file_description,
            "is_published": is_published,
        }

        empty_keys = [key for key in data.keys() if data[key] is None]
        for key in empty_keys:
            del data[key]
        return self.client.post(reverse("api:note-list"), data)

    def test_missing_usertoken_returns_403(self):
        response = self.post_request(note="missing token", token=None)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_usertoken_returns_403(self):
        response = self.post_request(note="wrong token", token=uuid.uuid4().hex)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_simple_note(self):
        response = self.post_request(
            note="drf test",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(Note.objects.get(content="drf test"))

    def test_file_upload(self):
        response = self.post_request(
            note="drf note with media",
            file=_file(),
            file_description="Drf description",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        note = Note.objects.get(content="drf note with media")
        file: RelatedFile = note.related_files.first()

        self.assertRegex(str(file.file), r"related/\d{4}/[-\w]+\.\w+$")
        self.assertEqual(file.description, "Drf description")


class DrfAddMediaToNoteTests(DrfTestCase):
    def test_append_media_to_existing_note(self):
        note = Note.objects.create(content_html="Hello")

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


def _file():
    return SimpleUploadedFile(
        "file.txt",
        b"__FILE_CONTENTS__",
        content_type="multipart/form-data",
    )
