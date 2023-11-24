import uuid

from basetest.testcase import BaseTestCase
from bma_app.models import ApiToken
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from main.models import Note, RelatedFile


class DrfCreateNoteTests(BaseTestCase):
    view_name = "api:note-list"

    def setUp(self) -> None:
        self.staff_user = User.objects.create_user(
            username="test-user-drf",
            is_staff=True,
        )
        self.non_staff_user = User.objects.create_user(username="anon")
        self.token = ApiToken.objects.create(
            user=self.staff_user, enabled=True
        ).uuid.hex

    def post_request(
        self,
        note: str = None,
        token: str = None,
        file: bool = False,
        file_description: str = None,
    ):
        data = self.create_data(note, token, file, file_description)
        response = self.client.post(reverse(self.view_name), data)
        return response

    def create_data(
        self,
        note: str = None,
        token: str = None,
        file: bool = False,
        file_description: str = None,
    ) -> dict:
        data = {
            "content": note or "",
            "token": token or "",
        }
        if file:
            data["file"] = SimpleUploadedFile("image-drf.txt", b"FileContents")
            data["file_description"] = file_description or ""

        return data

    def test_missing_usertoken_returns_403(self):
        response = self.post_request(note="missing token")
        self.assertEqual(response.status_code, 403)

    def test_wrong_usertoken_returns_403(self):
        response = self.post_request(note="wrong token", token=uuid.uuid4().hex)
        self.assertEqual(response.status_code, 403)

    def test_simple_note(self):
        response = self.post_request(
            note="drf test",
            token=self.token,
        )
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(Note.objects.get(content="drf test"))

    def test_file_upload(self):
        response = self.post_request(
            token=self.token,
            note="drf note with media",
            file=True,
            file_description="Drf description",
        )

        self.assertEqual(response.status_code, 201)
        note = Note.objects.get(content="drf note with media")
        file: RelatedFile = note.related_files.first()

        self.assertRegex(str(file.file), r"related/\d{4}/[-\w]+\.\w+$")
        self.assertEqual(file.description, "Drf description")
