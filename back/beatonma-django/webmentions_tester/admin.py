from common.admin import BaseAdmin
from django.contrib import admin
from webmentions_tester.models import TemporaryMention


@admin.register(TemporaryMention)
class TemporaryMentionAdmin(BaseAdmin):
    list_display = (
        "url",
        "outgoing_status",
        "submission_time",
        "is_expired",
    )
