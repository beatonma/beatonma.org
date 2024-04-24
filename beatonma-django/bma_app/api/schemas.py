from datetime import datetime
from typing import List
from uuid import UUID

from main.models.related_file import MediaType
from ninja import Schema
from pydantic import Field


class ApiEditableSchema(Schema):
    id: UUID = Field(alias="api_id")


class MediaSchema(ApiEditableSchema):
    url: str
    description: str
    type: MediaType


class NoteSchema(ApiEditableSchema):
    content_html: str
    content: str
    url: str = Field(alias="get_absolute_url")
    is_published: bool
    published_at: datetime
    media: List[MediaSchema] = Field(alias="related_files")
