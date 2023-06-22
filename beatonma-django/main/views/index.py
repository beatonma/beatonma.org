import logging

from common.views.logged import LoggedView
from django.core.paginator import Paginator
from django.shortcuts import render
from main.models import Note
from main.models.motd import MessageOfTheDay
from main.util import get_media_type_description
from main.views.querysets import get_main_feed

log = logging.getLogger(__name__)

ITEMS_PER_PAGE = 8


class IndexView(LoggedView):
    def get(self, request, *args, **kwargs):
        try:
            page = int(request.GET.get("page", 1))
        except ValueError:
            page = 1

        motd = MessageOfTheDay.objects.get_current()
        feed = get_main_feed()

        paginator = Paginator(feed, ITEMS_PER_PAGE)
        page_obj = paginator.get_page(page)

        return render(
            request,
            "pages/index/index.html",
            {
                "is_first_page": page == 1,
                "motd": motd,
                "feed": page_obj.object_list,
                "page_obj": page_obj,
            },
        )


def _get_media_for_note(note: Note):
    media = note.related_files.first()

    media_url = None
    media_description = None

    if media:
        media_url = media.file.url
        media_description = media.description

    return {
        "note": note,
        "media": {
            "url": media_url or "",
            "description": media_description or "",
            "type": get_media_type_description(media),
        },
    }
