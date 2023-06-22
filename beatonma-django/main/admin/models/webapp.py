from django import forms
from django.contrib import admin

from common.admin import BaseAdmin
from main.admin.models.posts.webpost import WebPostAdminForm
from main.models import WebApp


class WebAppAdminForm(forms.ModelForm):
    class Meta:
        model = WebApp
        fields = "__all__"


@admin.register(WebApp)
class WebAppAdmin(BaseAdmin):
    form = WebPostAdminForm
    list_display = [
        "title",
    ]
