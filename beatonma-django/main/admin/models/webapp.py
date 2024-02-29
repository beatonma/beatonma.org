from common.admin import BaseAdmin
from django import forms
from django.contrib import admin
from main.admin.models.posts.webpost import WebPostAdminForm
from main.models import WebApp
from main.models.webapp import WebappResource


class WebappResourceInline(admin.StackedInline):
    model = WebappResource
    extra = 1


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
    inlines = [WebappResourceInline]
