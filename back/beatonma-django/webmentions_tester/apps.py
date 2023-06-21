from django.apps import AppConfig


class WebmentionsTesterConfig(AppConfig):
    name = "webmentions_tester"

    def ready(self):
        # fmt: off
        from webmentions_tester.signals import (  # noqa
            update_temp_mention_when_outgoing_status_created
        )
        # fmt: on
