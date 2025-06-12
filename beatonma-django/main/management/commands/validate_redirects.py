import requests
from common.util.url import to_absolute_url
from django.contrib.redirects.models import Redirect
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        stale_redirects: list[Redirect] = []

        for redirect in Redirect.objects.all():
            path = redirect.new_path
            url = to_absolute_url(path)
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                self.stdout.write(f"OK {path}")
            else:
                stale_redirects.append(redirect)

        if stale_redirects:
            self.stdout.write("")
            self.stdout.write("Stale redirects:")
            for stale in stale_redirects:
                self.stdout.write(f"  {stale.new_path} ({stale.old_path})")
        else:
            self.stdout.write("All redirects resolve successfully!")
