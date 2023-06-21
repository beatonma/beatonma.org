import os.path

from django.core.management import BaseCommand

from webapp.wurdle.models import ValidWurd, Wurd


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--import_wurds",
            type=str,
        )

        parser.add_argument(
            "--import_valid_wurds",
            type=str,
        )

    def handle(self, *args, **options):
        if options.get("import_wurds"):
            _import_wurds(options["import_wurds"])

        elif options.get("import_valid_wurds"):
            _import_valid_wurds(options["import_valid_wurds"])

        else:
            print(f"Unhandled options {options}")


def _import_wurds(path):
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    day = 0
    last_wurd = Wurd.objects.last()
    if last_wurd:
        day = last_wurd.day + 1

    imported = 0
    with open(path, "r") as f:
        for wurd in f.readlines():
            wurd = wurd.strip()
            if len(wurd) != 5:
                raise ValueError(
                    f"Wurds must be 5 letters long (found '{wurd}'). Check file format!"
                )

            try:
                Wurd.objects.create(wurd=wurd, day=day)
                day += 1
                imported += 1
            except ValueError as e:
                print(f"Wurd '{wurd}' skipped: {e}")

    print(f"Imported {imported} wurds")


def _import_valid_wurds(path):
    print(path)
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    imported = 0
    with open(path, "r") as f:
        for wurd in f.readlines():
            wurd = wurd.strip()
            if len(wurd) != 5:
                raise ValueError(
                    f"Wurds must be 5 letters long (found '{wurd}'). Check file format!"
                )

            try:
                ValidWurd.objects.create(wurd=wurd)
                imported += 1
            except ValueError as e:
                print(f"ValidWurd '{wurd}' skipped: {e}")

    print(f"Imported {imported} valid wurds")
