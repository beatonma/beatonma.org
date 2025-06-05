from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.http import HttpRequest
from main.models import Post
from ninja import Router, Schema
from taggit.models import Tag

router = Router(tags=["Tags"])


class TagDetail(Schema):
    name: str
    count: int


@router.get("/tags/", response=list[TagDetail])
def tags(request: HttpRequest):
    content_types = ContentType.objects.get_for_models(*Post.subclasses()).values()
    return Tag.objects.filter(
        taggit_taggeditem_items__content_type__in=content_types
    ).annotate(count=Count("taggit_taggeditem_items"))
