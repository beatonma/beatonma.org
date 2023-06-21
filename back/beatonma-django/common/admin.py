from typing import List, Type

from django.apps import apps
from django.contrib import admin
from django.db import models
from django.forms import Textarea

from beatonma.settings import environment


class BaseAdmin(admin.ModelAdmin):
    """Base implementation of ModelAdmin for all admin pages in the project.

    Attributes:
        admin_app_priority  Weighting applied when ordering apps for display on
                            root Admin page. Lower values come first.
        admin_priority      Weighting applied when ordering models for display
                            on admin pages. Lower values come first.
    """

    admin_app_priority = 20
    admin_priority = 20
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


def _get_app_list(self, request):
    app_dict = self._build_app_dict(request)
    from django.contrib.admin.sites import site

    app_ordering = {key: 1000 for key in app_dict.keys()}

    for app_name, app in app_dict.items():
        for model in app["models"]:
            app_ordering[app_name] = min(
                app_ordering[app_name],
                getattr(
                    site._registry[apps.get_model(app_name, model["object_name"])],
                    "admin_app_priority",
                    1000,
                ),
            )

    for app_name in sorted(app_ordering.keys(), key=lambda x: app_ordering[x]):
        app = app_dict[app_name]
        model_priority = {
            model["object_name"]: getattr(
                site._registry[apps.get_model(app_name, model["object_name"])],
                "admin_priority",
                20,
            )
            for model in app["models"]
        }
        app["models"].sort(key=lambda x: model_priority[x["object_name"]])
        yield app


admin.AdminSite.get_app_list = _get_app_list
