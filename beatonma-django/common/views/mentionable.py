from common.views import BaseView
from django.http import HttpRequest
from mentions import contract


class MentionableView(BaseView):
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        for key in [
            contract.URLPATTERNS_MODEL_NAME,
            contract.URLPATTERNS_MODEL_FILTERS,
            contract.URLPATTERNS_MODEL_FILTER_MAP,
        ]:
            if key in kwargs:
                kwargs.pop(key)

        return super().dispatch(request, *args, **kwargs)
