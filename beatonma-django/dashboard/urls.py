import logging

from django.urls import path

from dashboard.views import DashboardApiView, DashboardView
from dashboard.views.checks import CeleryTaskTestView

log = logging.getLogger(__name__)


urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("status/", DashboardApiView.as_view(), name="dashboard-api"),
    path("celery/", CeleryTaskTestView.as_view(), name="celery-check"),
]
