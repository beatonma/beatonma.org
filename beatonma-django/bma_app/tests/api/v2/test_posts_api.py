import re
import uuid
from datetime import datetime

from bma_app import auth
from bma_app.api import api
from bma_app.api.util import no_null_dict
from bma_app.tests.api.v2.test_api import ApiTestCase
from common.models.generic import generic_fk
from common.util import http
from common.util.time import tzdatetime
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.urls import reverse
from main.models import Post, RelatedFile

api_namespace = api.urls_namespace
endpoint_posts = reverse(f"{api_namespace}:get_posts")


def endpoint_post(post_id: uuid.UUID):
    return reverse(f"{api_namespace}:get_post", args=[post_id])


def endpoint_media(media_id: uuid.UUID):
    return reverse(f"{api_namespace}:get_media", args=[media_id])


def endpoint_create_media_for_post(post_id: uuid.UUID):
    return reverse(f"{api_namespace}:add_media_to_post", args=[post_id])


class GetPostTests(ApiTestCase):
    def test_post_structure_is_correct(self):
        post = Post.objects.create(content="This is content")
        file = RelatedFile.objects.create(
            file=_file(), description="file description", **generic_fk(post)
        )

        response = self.get_with_api_token(endpoint_post(post.api_id))
        data = response.json()

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
        self.assertEqual(data["id"], str(post.api_id))

        self.assertRegex(data["media"][0]["id"], uuid_pattern)
        self.assertEqual(data["media"][0]["id"], str(file.api_id))


class CreatePostTests(ApiTestCase):
    def post_request(
        self,
        content: str = None,
        token: str | bool | None = True,
        file: File | None = None,
        file_description: str | None = None,
        is_published: bool = True,
        published_at: datetime | None = None,
        post_id: str | None = None,
    ) -> HttpResponse:
        data = no_null_dict(
            **{
                auth.TOKEN_KEY: self.token if token is True else token,
                "id": post_id,
                "content": content,
                "file": file,
                "file_description": file_description,
                "is_published": is_published,
                "published_at": published_at,
            }
        )

        return self.client.post(endpoint_posts, data)

    def test_missing_usertoken_returns_401(self):
        response = self.post_request(content="missing token", token=None)
        self.assertEqual(response.status_code, http.STATUS_401_UNAUTHORIZED)

    def test_wrong_usertoken_returns_401(self):
        response = self.post_request(content="wrong token", token=uuid.uuid4().hex)
        self.assertEqual(response.status_code, http.STATUS_401_UNAUTHORIZED)

    def test_create_simple_post(self):
        response = self.post_request(content="api test")
        self.assertEqual(response.status_code, http.STATUS_201_CREATED)
        self.assertIsNotNone(Post.objects.get(content="api test"))

    def test_create_post_with_custom_published_at(self):
        response = self.post_request(
            content="custom published at",
            published_at=datetime(2023, 12, 20, 18, 0, 0),
        )

        self.assertEqual(response.status_code, http.STATUS_201_CREATED)
        post = Post.objects.get(content="custom published at")
        self.assertEqual(
            post.published_at,
            tzdatetime(2023, 12, 20, 18, 0, 0),
        )

    def test_create_post_with_media(self):
        response = self.post_request(
            content="api post with media",
            file=_file(),
            file_description="Drf description",
        )

        self.assertEqual(response.status_code, http.STATUS_201_CREATED)
        post = Post.objects.get(content="api post with media")
        file: RelatedFile = post.related_files.first()

        self.assertRegex(str(file.file), r"related/\d{4}/[-\w]+\.\w+$")
        self.assertEqual(file.description, "Drf description")

    def test_edit_post_partial(self):
        post = Post.objects.create(content="unchanged :)", is_published=False)
        response = self.patch_with_api_token(
            endpoint_post(post.api_id),
            {
                "is_published": True,
            },
        )
        post.refresh_from_db()
        self.assertEqual(response.status_code, http.STATUS_200_OK)
        self.assertEqual(post.content, "unchanged :)")
        self.assertTrue(post.is_published)

        response = self.patch_with_api_token(
            endpoint_post(post.api_id),
            {
                "is_published": False,
            },
        )
        post.refresh_from_db()
        self.assertEqual(response.status_code, http.STATUS_200_OK)
        self.assertFalse(post.is_published)

    def test_delete_post(self):
        post = Post.objects.create(content="delete this")
        response = self.delete_with_api_token(endpoint_post(post.api_id))

        self.assertEqual(response.status_code, http.STATUS_204_NO_CONTENT)
        with self.assertRaises(Post.DoesNotExist):
            post.refresh_from_db()


class PostMediaTests(ApiTestCase):
    def test_append_media_to_existing_post(self):
        post = Post.objects.create(content="Hello")

        response = self.client.post(
            endpoint_create_media_for_post(post.api_id),
            {
                "token": self.token,
                "file": _file(),
                "file_description": "Added later",
            },
        )

        self.assertEqual(response.status_code, http.STATUS_201_CREATED)
        file: RelatedFile = post.related_files.first()

        self.assertEqual(file.description, "Added later")

    def test_delete_media(self):
        post = Post.objects.create(content="delete the media")
        file = RelatedFile.objects.create(file=_file(), **generic_fk(post))

        response = self.delete_with_api_token(endpoint_media(file.api_id))
        self.assertEqual(response.status_code, http.STATUS_204_NO_CONTENT)
        with self.assertRaises(RelatedFile.DoesNotExist):
            file.refresh_from_db()

    def test_update_media(self):
        post = Post.objects.create(content="delete the media")
        file = RelatedFile.objects.create(
            file=_file(), description="unedited", **generic_fk(post)
        )

        response = self.patch_with_api_token(
            endpoint_media(file.api_id),
            {
                "description": "edited!",
            },
        )
        self.assertEqual(response.status_code, http.STATUS_200_OK)
        file.refresh_from_db()
        self.assertEqual(file.description, "edited!")


def _file():
    return SimpleUploadedFile(
        "file.txt",
        b"__FILE_CONTENTS__",
        content_type="multipart/form-data",
    )
