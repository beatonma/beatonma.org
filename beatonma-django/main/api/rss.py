from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from main.api.querysets import get_feed, get_feed_filters


class LatestUpdatesRichFeed(Rss201rev2Feed):
    def rss_attributes(self):
        attrs = super().rss_attributes()
        attrs["xmlns:webfeeds"] = "http://webfeeds.org/rss/1.0"
        return attrs

    def add_root_elements(self, handler):
        super().add_root_elements(handler)

        for key in ["webfeeds:icon", "webfeeds:logo", "webfeeds:cover image"]:
            handler.addQuickElement(key, "https://beatonma.org/static/images/mb.svg")

        handler.addQuickElement("webfeeds:accentColor", "ff4081")


class LatestUpdatesFeed(Feed):
    title = "beatonma.org"
    link = "https://beatonma.org"
    author_name = "Michael Beaton"
    description = "Projects and utterings."
    language = "en-gb"

    feed_type = LatestUpdatesRichFeed

    def get_object(self, request, *args, **kwargs):
        self.filters = get_feed_filters(request.GET)
        return None

    def items(self):
        feed = get_feed(**self.filters)
        del self.filters
        return feed

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.preview_html or item.content_html
