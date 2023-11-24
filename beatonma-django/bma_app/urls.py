from bma_app.views.api import check_request_token
from bma_app.views.notes import NotesViewSet
from bma_app.views.whoami import WhoamiView
from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import APIRootView as DrfRootView


class ApiRootView(DrfRootView):
    def get(self, request, *args, **kwargs):
        return check_request_token(request) or super().get(request, *args, **kwargs)


class Router(routers.DefaultRouter):
    APIRootView = ApiRootView


router = Router()
router.register("notes", NotesViewSet)


app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
    path("whoami/", WhoamiView.as_view(), name="whoami"),
]
