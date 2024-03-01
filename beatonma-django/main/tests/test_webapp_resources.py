from basetest.testcase import LocalTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from main.models import WebApp
from main.models.webapp import WebappResource


class WebpostResourceTests(LocalTestCase):
    def test_webapp_with_resources_is_moved_to_own_directory(self):
        script = SimpleUploadedFile("script.js", b"const a = 1;")
        resource = SimpleUploadedFile("resource.txt", b"Hello World!")

        app = WebApp.objects.create(title="title", slug="slug", script=script)
        self.assertTrue(
            app.script.path.endswith("webapps/script.js"), msg=app.script.path
        )

        res = WebappResource.objects.create(webapp=app, file=resource)

        self.assertTrue(
            app.script.path.endswith("webapps/slug/script.js"), msg=app.script.path
        )
        self.assertTrue(
            res.file.path.endswith("webapps/slug/resource.txt"), msg=res.file.path
        )
