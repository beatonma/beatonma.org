from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from main.views.querysets import get_main_feed


class LatestUpdatesRichFeed(Rss201rev2Feed):
    def rss_attributes(self):
        attrs = super(LatestUpdatesRichFeed, self).rss_attributes()
        attrs["xmlns:webfeeds"] = "http://webfeeds.org/rss/1.0"
        return attrs

    def add_root_elements(self, handler):
        super(LatestUpdatesRichFeed, self).add_root_elements(handler)

        for key in ["webfeeds:icon", "webfeeds:logo", "webfeeds:cover image"]:
            handler.addQuickElement(key, "https://beatonma.org/static/images/mb.svg")

        handler.addQuickElement("webfeeds:accentColor", "ff4081")


class LatestUpdatesFeed(Feed):
    title = "beatonma.org"
    link = "https://beatonma.org"
    description = "Software and electronics projects."

    feed_type = LatestUpdatesRichFeed

    def items(self):
        return get_main_feed()

    def item_title(self, item):
        return choose_attribute(item, "title", "name", default="")

    def item_description(self, item):
        return choose_attribute(item, "preview_text", "description", default="")


def choose_attribute(item, *names: str, default=None):
    for name in names:
        if hasattr(item, name):
            return getattr(item, name)

    return default
