from django.urls import path

from webapp.wurdle.views import GuessView, WurdView

urlpatterns = [
    path("wurd", WurdView.as_view(), name="wurdle-rules"),
    path("guess", GuessView.as_view(), name="wurdle-guess"),
]
