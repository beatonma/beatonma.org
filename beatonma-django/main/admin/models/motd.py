from common.admin import BaseAdmin
from django.contrib import admin
from main.models import MessageOfTheDay


@admin.register(MessageOfTheDay)
class MotdAdmin(BaseAdmin):
    editable_fields = ["content", "public_from", "public_until", "is_published"]
    field_groups = [
        ["public_from", "public_until"],
    ]
