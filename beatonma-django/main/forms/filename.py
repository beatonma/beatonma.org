import os
import uuid
from typing import Callable

from django.utils.deconstruct import deconstructible
from django.utils.text import slugify


@deconstructible
class RandomFilename:
    def __init__(
        self,
        upload_to: str | Callable,
        filename_literals: list[str] = None,
        filename_attrs: list[str] = None,
    ):
        self.upload_to = upload_to
        self.filename_attrs = filename_attrs or []
        self.filename_literals = filename_literals or []

    def __call__(self, instance, original_filename) -> str:
        parts = original_filename.split(".")
        ext = parts[-1]

        chunks: list[str] = ["-".join(self.filename_literals)]

        if not instance:
            # No instance attributes if instance is null
            pass

        elif self.filename_attrs:
            attrs = [getattr(instance, attr, None) for attr in self.filename_attrs]
            chunks += [x for x in attrs if x]

        else:
            slug = _get_slug(instance)
            if slug:
                chunks.append(slug[:20])

        uid = uuid.uuid4().hex[:6]
        chunks.append(uid)
        basename = "-".join(chunk for chunk in chunks if chunk)
        basename = slugify(basename[:30])
        filename = f"{basename}.{ext}"

        if callable(self.upload_to):
            return self.upload_to(instance, filename)

        return os.path.join(self.upload_to, filename)

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        if callable(self.upload_to) and callable(other.upload_to):
            if self.upload_to.__name__ != other.upload_to.__name__:
                return False

        elif self.upload_to != other.upload_to:
            return False

        return (
            self.filename_attrs == other.filename_attrs
            and self.filename_literals == other.filename_literals
        )


def _get_slug(instance) -> str | None:
    slug = getattr(instance, "slug", None)
    if slug:
        return slug

    target = getattr(instance, "target_object", None)
    if target:
        return getattr(target, "slug", None)

    return None
