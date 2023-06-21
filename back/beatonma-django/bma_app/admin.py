from bma_app.models import ApiToken
from common.admin import BaseAdmin
from django.contrib import admin


@admin.register(ApiToken)
class ApiTokenAdmin(BaseAdmin):
    pass
