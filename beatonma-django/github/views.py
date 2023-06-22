from django.http import JsonResponse
from django.views import View
from github.models import CachedResponse


class GithubEventsView(View):
    def get(self, request, *args, **kwargs):
        cached_response = CachedResponse.objects.first()

        events = cached_response.data if cached_response else []

        return JsonResponse(
            {
                "events": events,
            }
        )
