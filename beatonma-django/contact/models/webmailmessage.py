import logging

from common.models import ApiModel, BaseModel
from django.db import models
from django.db.models import QuerySet

log = logging.getLogger(__name__)


class WebmailQuerySet(QuerySet):
    def filter_unread(self):
        return self.filter(has_been_read=False)

    def mark_as_read(self):
        return self.update(has_been_read=True)

    def mark_as_unread(self):
        return self.update(has_been_read=False)


class WebmailMessage(ApiModel, BaseModel):
    objects = WebmailQuerySet.as_manager()

    name = models.CharField(blank=True, max_length=256)
    contact = models.CharField(blank=True, max_length=256)
    subject = models.CharField(blank=True, max_length=256)
    message_body = models.TextField(blank=True)

    has_been_read = models.BooleanField(default=False)

    def mark_as_read(self):
        self.has_been_read = True
        self.save()

    @classmethod
    def create_from_http_post(cls, http_post):
        msg = WebmailMessage.objects.create(
            name=http_post.get("name", "No name given"),
            contact=http_post.get("contact_method", "No contact info given"),
            subject=http_post.get("subject", "beatonma.org webmail"),
            message_body=http_post.get("message", "No message given"),
        )
        return msg

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "contact": self.contact,
            "body": self.message_body,
            "timestamp": self.created_at,
        }

    def __str__(self):
        return f"{self.name}: {self.subject}"
