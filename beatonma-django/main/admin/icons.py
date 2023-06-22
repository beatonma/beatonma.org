from django.utils.safestring import mark_safe


def admin_icon_check() -> str:
    return mark_safe('<img src="/static/admin/img/icon-yes.svg" alt="True"/>')


def admin_icon_cross() -> str:
    return mark_safe('<img src="/static/admin/img/icon-no.svg" alt="False"/>')
