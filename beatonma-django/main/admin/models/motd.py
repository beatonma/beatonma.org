from django.contrib import admin

from common.admin import BaseAdmin
from main.models import MessageOfTheDay


@admin.register(MessageOfTheDay)
class MotdAdmin(BaseAdmin):
    pass
