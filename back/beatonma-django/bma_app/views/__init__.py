import logging

from bma_app.models import ApiToken
from common.views.api import ApiView
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

log = logging.getLogger(__name__)


class AppApiView(ApiView):
    @csrf_exempt
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        data = request.POST

        usertoken = data.get("token")
        if not usertoken:
            log.warning(f"Missing API token: {data}")
            return HttpResponse(status=403)

        token = ApiToken.objects.filter(uuid=usertoken).first()
        if not token or not token.enabled:
            log.warning(f"Bad API token: {token}")
            return HttpResponse(status=403)

        if not token.user.is_staff:
            log.warning(f"Bad API token user: {token.user}")
            return HttpResponse(status=403)

        return super().dispatch(request, *args, **kwargs)


from .notes import CreateNoteView
