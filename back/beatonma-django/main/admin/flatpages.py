import os

from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin, FlatpageForm
from django.contrib.flatpages.models import FlatPage
from django.db import models
from django.forms.widgets import Textarea

admin.site.unregister(FlatPage)


class TemplateChoicesFlatpageForm(FlatpageForm):
    template_name = forms.ChoiceField(
        choices=[
            # (f"flatpages/{x}", x)
            # for x in sorted(os.listdir(settings.BASE_DIR / "main/templates/flatpages/"))
        ]
    )


@admin.register(FlatPage)
class DefaultFlatpageAdmin(FlatPageAdmin):
    save_on_top = True
    form = TemplateChoicesFlatpageForm

    formfield_overrides = {
        models.CharField: {
            "widget": Textarea(attrs={"rows": 2, "cols": 80}),
        },
        models.TextField: {
            "widget": Textarea(attrs={"rows": 10, "cols": 80}),
        },
    }
