from datetime import datetime

from mentions.models.mixins import IncomingMentionType
from ninja import Schema
from pydantic import Field


class HCard(Schema):
    name: str | None
    avatar: str | None = Field(alias="avatar", default=None)
    homepage: str | None


class Mention(Schema):
    source_url: str
    hcard: HCard | None
    quote: str | None
    type: IncomingMentionType | str | None = Field(alias="post_type", default=None)
    date: datetime = Field(alias="published")
