from bma_app.views.api import ApiTokenPermission
from bma_app.views.notes import MediaViewSet, NotesViewSet
from bma_app.views.whoami import WhoamiView
from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import APIRootView as DrfRootView


class ApiRootView(DrfRootView):
    permission_classes = (ApiTokenPermission,)


class Router(routers.DefaultRouter):
    APIRootView = ApiRootView


router = Router()
router.register("notes", NotesViewSet)
router.register("media", MediaViewSet)


app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
    path("whoami/", WhoamiView.as_view(), name="whoami"),
]
