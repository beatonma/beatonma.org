import os

from basetest.testcase import LocalTestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from main.models import WebApp
from main.models.webapp import WebappResource


class WebpostResourceTests(LocalTestCase):
    def setUp(self):
        self.script = SimpleUploadedFile("script.js", b"const a = 1;")
        self.resource = SimpleUploadedFile("resource.txt", b"Hello World!")

    def test_webapp_with_resources_is_moved_to_own_directory(self):
        app = WebApp.objects.create(title="title", slug="slug", script=self.script)
        self.assertTrue(
            app.script.path.endswith("webapps/script.js"),
            msg=app.script.path,
        )

        res = WebappResource.objects.create(webapp=app, file=self.resource)
        self.assertTrue(
            app.script.path.endswith("webapps/slug/script.js"),
            msg=app.script.path,
        )
        self.assertTrue(
            res.file.path.endswith("webapps/slug/resource.txt"),
            msg=res.file.path,
        )

    def test_resources_zip(self):
        from zipfile import ZipFile

        xml_path = os.path.join(settings.MEDIA_ROOT, "string.xml")
        zip_path = os.path.join(settings.MEDIA_ROOT, "resources.zip")

        with open(xml_path, "w") as f:
            f.write("xml resource")

        with ZipFile(zip_path, "w") as zip:
            zip.write(xml_path)

        with open(zip_path, "rb") as zip:
            WebApp.objects.create(
                title="title",
                slug="slug",
                script=SimpleUploadedFile("resources.zip", zip.read()),
            )

        resource = WebappResource.objects.get(file__endswith="string.xml")
        with open(resource.file.path, "r") as f:
            content = f.read()
        self.assertEqual(content, "xml resource")
