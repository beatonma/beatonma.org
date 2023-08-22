import logging

from django.core.management import BaseCommand

log = logging.getLogger(__name__)


class AsyncCommand(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "-instant",
            action="store_true",
            default=False,
            help="Run the task synchronously.",
        )

    def handle_async(self, func, func_kwargs=None, **command_options):
        """Call from handle(), passing the function along with the received options.
        e.g.
        def handle(self, *args, **options):
            self.handle_async(myfunc, func_kwargs={'whatever': True}, **command_options)
        Any arguments for the func should be in func_kwargs, not command_options.
        """
        if func_kwargs is None:
            func_kwargs = {}

        assert hasattr(func, "delay"), (
            "AsyncCommand.handle_async received a function that is not registered"
            f"as a task: {func.__name__}"
        )

        if command_options.get("instant") is True:
            print(
                f"Launching function `{func}` synchronously with kwargs={func_kwargs}."
            )
            func(**func_kwargs)
        else:
            log.info(
                f"Dispatching function `{func}` to worker with kwargs={func_kwargs}."
            )
            func.delay(**func_kwargs)
