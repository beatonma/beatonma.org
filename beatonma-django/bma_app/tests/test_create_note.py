from basetest.testcase import BaseTestCase
from bma_app.models import ApiToken
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from main.models import Note, RelatedFile


class CreateNoteTests(BaseTestCase):
    def create_data(
        self,
        note: str = None,
        token: str = None,
        file: bool = False,
        file_description: str = None,
    ) -> dict:
        data = {}
        if note is not None:
            data["content"] = note

        if token is not None:
            data["token"] = token

        if file:
            data["file"] = SimpleUploadedFile("image.txt", b"FileContents")

        if file_description:
            data["description"] = file_description

        return data

    def post_request(self, data: dict):
        return self.client.post(
            reverse("bma_app_create_note"),
            data=data,
        )

    def setUp(self) -> None:
        self.note_content = "This is note content"
        self.staff_user = User.objects.create_user(username="test-user", is_staff=True)
        self.token = ApiToken.objects.create(user=self.staff_user, enabled=True)

    def test_successful(self):
        response = self.post_request(
            self.create_data(self.note_content, self.token.uuid),
        )

        self.assertEqual(response.status_code, 200)
        created_note = self.assert_exists(Note, content="This is note content")
        self.assertEqual(response.json().get("id"), created_note.pk)

    def test_missing_usertoken_returns_403(self):
        response = self.post_request(self.create_data(self.note_content))
        self.assertEqual(response.status_code, 403)

    def test_missing_note_returns_400(self):
        response = self.post_request(self.create_data(token=self.token.uuid))

        self.assertEqual(response.status_code, 400)

    def test_file_upload(self):
        response = self.post_request(
            self.create_data(
                token=self.token.uuid, file=True, file_description="Description"
            )
        )

        self.assertEqual(response.status_code, 200)
        note = Note.objects.first()
        file: RelatedFile = note.related_files.first()

        self.assertRegex(str(file.file), r"related/\d{4}/[-\w]+\.txt$")
        self.assertEqual(file.description, "Description")
