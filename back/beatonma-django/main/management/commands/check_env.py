from django.conf import settings
from django.core.management import BaseCommand

REQUIRED_FIELDS = [
    "DOMAIN_NAME",
    "DOMAIN_EMAIL",
    "SITE_NAME",
    "SECRET_KEY",
    "GITHUB_ACCESS_TOKEN",
    "GITHUB_USERNAME",
    "FCM_API_KEY",
    "GOOGLE_RECAPTCHA_SECRET",
    "CELERY_BROKER_URL",
    "ADMIN_NAME",
    "ADMIN_EMAIL",
    "ADMIN_URL",
    "DASHBOARD_URL",
    "BMA_NOTIFICATIONS_URL",
    "BMA_NOTIFICATIONS_ACCOUNT",
    "SERVER_EMAIL",
    "EMAIL_HOST",
    "EMAIL_PORT",
    "EMAIL_HOST_USER",
    "EMAIL_HOST_PASSWORD",
    "WEBMAIL_CONTACT_EMAIL",
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for field in REQUIRED_FIELDS:
            assert hasattr(settings, field), f"settings.{field} is missing"
            assert (
                getattr(settings, field, None) is not None
            ), f"settings.{field} is None"
