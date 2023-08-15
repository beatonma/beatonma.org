import os

from beatonma.settings.templates import get_flatpage_templates
from django import forms
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin, FlatpageForm
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.views import DEFAULT_TEMPLATE
from django.contrib.sites.models import Site
from django.db import models
from django.forms.widgets import Textarea
from django.utils.translation import gettext_lazy as _

admin.site.unregister(FlatPage)


class TemplateChoicesFlatpageForm(FlatpageForm):
    template_name = forms.ChoiceField(
        choices=lambda: [
            (x, os.path.basename(x)) for x in sorted(get_flatpage_templates())
        ],
        initial=DEFAULT_TEMPLATE,
    )

    sites = forms.ModelMultipleChoiceField(
        queryset=Site.objects.all(),
        initial=Site.objects.all(),
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

    fieldsets = (
        (None, {"fields": ("url", "title", "content", "template_name")}),
        (
            _("Advanced options"),
            {
                "classes": ("collapse",),
                "fields": ("registration_required", "sites"),
            },
        ),
    )
