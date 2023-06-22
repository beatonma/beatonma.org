from bma_dev.views import DevThemeView
from common.urls import path

urlpatterns = [
    path("theme-preview/", DevThemeView),
]
