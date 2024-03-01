import os

from basetest.testcase import LocalTestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from main.models import WebApp
from main.models.webapp import WebappResource


class WebpostResourceTests(LocalTestCase):
    def test_webapp_with_resources_is_moved_to_own_directory(self):
        app = WebApp.objects.create(
            title="title",
            slug="slug",
            file=SimpleUploadedFile("script.js", b"const a = 1;"),
        )
        self.assertTrue(
            app.file.path.endswith("webapps/script.js"),
            msg=app.file.path,
        )

        res = WebappResource.objects.create(
            webapp=app, file=SimpleUploadedFile("resource.txt", b"Hello World!")
        )
        self.assertTrue(
            app.file.path.endswith("webapps/slug/script.js"),
            msg=app.file.path,
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
            zip.write(xml_path, arcname="string.xml")

        with open(zip_path, "rb") as zip:
            webapp = WebApp.objects.create(
                title="title",
                slug="slug",
                file=SimpleUploadedFile("script.js", b"const b = 2;"),
            )
            WebappResource.objects.create(
                webapp=webapp,
                file=SimpleUploadedFile("resources.zip", zip.read()),
            )

        resource = WebappResource.objects.get(file__endswith="string.xml")
        with open(resource.file.path, "r") as f:
            content = f.read()
        self.assertEqual(content, "xml resource")

        self.assertEqual(1, WebappResource.objects.all().count())

    def tearDown(self):
        for path in ["resources.zip", "string.xml"]:
            path = os.path.join(settings.MEDIA_ROOT, path)
            if os.path.exists(path):
                os.remove(path)
