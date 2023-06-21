from common.admin import BaseAdmin
from contact.models.webmailmessage import WebmailMessage
from django.contrib import admin


@admin.action(description="Mark as read")
def action_mark_as_read(modeladmin, request, queryset):
    queryset.mark_as_read()


@admin.action(description="Mark as unread")
def action_mark_as_unread(modeladmin, request, queryset):
    queryset.mark_as_unread()


@admin.register(WebmailMessage)
class WebmailMessageAdmin(BaseAdmin):
    admin_app_priority = 0

    def truncated_message_body(self, message: WebmailMessage) -> str:
        return message.message_body[:140]

    actions = [
        action_mark_as_read,
        action_mark_as_unread,
    ]

    list_display = [
        "created_at",
        "has_been_read",
        "name",
        "truncated_message_body",
    ]

    readonly_fields = [
        "name",
        "contact",
        "subject",
        "message_body",
        "created_at",
        "truncated_message_body",
    ]
