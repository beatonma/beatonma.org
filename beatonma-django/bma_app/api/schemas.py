from datetime import datetime
from uuid import UUID

from main.models.mixins.media_upload import MediaType
from ninja import Schema
from pydantic import Field


class ApiEditableSchema(Schema):
    id: UUID = Field(alias="api_id")


class MediaSchema(ApiEditableSchema):
    url: str
    description: str
    type: MediaType


class PostSchema(ApiEditableSchema):
    content_html: str
    content: str
    url: str = Field(alias="get_absolute_url")
    is_published: bool
    published_at: datetime
    media: list[MediaSchema] = Field(alias="related_files")
