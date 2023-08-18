from typing import List, Type

from beatonma.settings import environment
from django.apps import apps
from django.contrib import admin
from django.db import models
from django.forms import Textarea


class BaseAdmin(admin.ModelAdmin):
    """Base implementation of ModelAdmin for all admin pages in the project."""

    save_on_top = True

    formfield_overrides = {
        models.CharField: {
            "widget": Textarea(attrs={"rows": 2, "cols": 80, "class": "charfield"}),
        },
        models.TextField: {
            "widget": Textarea(attrs={"rows": 20, "cols": 80}),
        },
    }

    class Media:
        js = ()
        css = {
            "all": (f"/static/css/admin-{environment.GIT_HASH}.min.css",),
        }

    def get_model_fields(self, Model: models.Model):
        return Model._meta.fields


def get_module_models(module_name: str) -> List[models.Model]:
    repository_config = apps.get_app_config(module_name)
    return repository_config.get_models()


def register_models_to_default_admin(
    module_name: str,
    default_admin: Type[admin.ModelAdmin],
):
    """
    Any models in the module that have not already been registered will be registered with default_admin.
    """
    for model in get_module_models(module_name):
        try:
            admin.site.register(model, default_admin)
        except admin.sites.AlreadyRegistered:
            pass


def _get_app_list(self, request, app_label=None):
    """
    Return a sorted list of all the installed apps that have been
    registered in this site.

    This implementation moves the apps in 'priority_apps' to the top for easy access.
    """
    app_dict = self._build_app_dict(request, app_label)

    priority_apps = [
        "contact",
        "main",
        "flatpages",
        "github",
        "bma_app",
        "bma_dev",
    ]

    # Sort the apps alphabetically.
    app_list = sorted(
        [x for x in app_dict.values() if x["app_label"] in priority_apps],
        key=lambda x: priority_apps.index(x["app_label"]),
    ) + sorted(
        [x for x in app_dict.values() if x["app_label"] not in priority_apps],
        key=lambda x: x["name"].lower(),
    )

    # Sort the models alphabetically within each app.
    for app in app_list:
        app["models"].sort(key=lambda x: x["name"])

    return app_list


admin.AdminSite.get_app_list = _get_app_list
