from bma_app.views import CreateNoteView
from bma_app.views.whoami import WhoamiView
from django.urls import path

urlpatterns = [
    path("create/note/", CreateNoteView.as_view(), name="bma_app_create_note"),
    path("whoami/", WhoamiView.as_view(), name="bma_app_whoami"),
]
