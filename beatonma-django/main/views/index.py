import logging

from common.views.logged import LoggedView
from django.shortcuts import render
from main.models.motd import MessageOfTheDay
from main.views.querysets import get_main_feed
from main.views.util.pagination import paginate

log = logging.getLogger(__name__)


class IndexView(LoggedView):
    def get(self, request, *args, **kwargs):
        motd = MessageOfTheDay.objects.get_current()
        feed = get_main_feed()
        paginated_context = paginate(request, feed)

        return render(
            request,
            "pages/index/index.html",
            {
                "motd": motd,
                **paginated_context,
            },
        )
