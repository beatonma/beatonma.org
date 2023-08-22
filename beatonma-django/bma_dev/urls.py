from bma_dev.views import DevThemeView, SimulatedErrorView
from common.urls import path

urlpatterns = [
    path("theme-preview/", DevThemeView),
    path("error/<int:error_code>/", SimulatedErrorView),
]
