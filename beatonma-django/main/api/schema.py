from main.models.related_file import BaseUploadedFile, MediaType
from ninja import Field, Schema

type Url = str


class File(Schema):
    url: Url = Field(alias="file_or_none.url")
    thumbnail_url: Url = Field(alias="thumbnail_or_none.url", default=None)
    type: MediaType
    name: str | None = Field(alias="original_filename", default=None)
    description: str | None
    fit: BaseUploadedFile.ImageFit | None


class Link(Schema):
    url: str
    label: str | None = None
    description: str | None = None
    icon: Url | None = Field(alias="host.icon_file", default=None)
