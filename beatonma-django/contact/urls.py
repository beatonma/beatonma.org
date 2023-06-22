from django.urls import path
from django.views.generic import TemplateView

from .views import ContactApiView

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="contact.html"),
        name="contact_form_view",
    ),
    path("send/", ContactApiView.as_view(), name="contact_api_view"),
]
