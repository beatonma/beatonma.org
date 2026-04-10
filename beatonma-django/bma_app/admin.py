from django.contrib import admin

from bma_app.models import ApiToken
from common.admin import BaseAdmin


@admin.register(ApiToken)
class ApiTokenAdmin(BaseAdmin):
    pass
