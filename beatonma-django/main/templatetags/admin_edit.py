import logging

from django import template
from django.urls import reverse

log = logging.getLogger(__name__)
register = template.Library()


@register.filter(name="admin_edit_url")
def admin_edit_url(model) -> str:
    if not model:
        return ""
    result = f"admin:{model._meta.app_label}_{model._meta.model_name}_change"
    return reverse(result, args=[model.pk])
