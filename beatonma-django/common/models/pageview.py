from common.models import BaseModel
from common.models.api import ApiModel
from django.db import models


class PageView(ApiModel, BaseModel):
    url = models.URLField(max_length=500)
    ip = models.CharField(max_length=255, null=True, blank=True)

    ua_device = models.CharField(max_length=255, null=True, blank=True)
    ua_os = models.CharField(max_length=255, null=True, blank=True)
    ua_browser = models.CharField(max_length=255, null=True, blank=True)

    def ua(self):
        return f"{self.ua_device}/{self.ua_os}/{self.ua_browser}"

    def __str__(self):
        return f"{self.url}: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        ordering = ["-created_at"]

    def to_json(self) -> dict:
        return {
            "url": self.url,
            "timestamp": self.created_at,
            "ip": self.ip,
            "device": self.ua_device,
            "os": self.ua_os,
            "browser": self.ua_browser,
        }
