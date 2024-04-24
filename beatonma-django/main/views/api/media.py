import logging
from typing import Union

from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic.base import View
from main.models.related_file import RelatedFilesMixin
from mentions.models.mixins import MentionableMixin
from mentions.resolution import get_model_for_url

log = logging.getLogger(__name__)


class RelatedFilesJsonView(View):
    def get(self, request, *args, **kwargs):
        url = request.GET.get("url")

        if url is None:
            return HttpResponseBadRequest("Missing required url.")

        try:
            model: Union[RelatedFilesMixin, MentionableMixin] = get_model_for_url(url)
            related_files = model.related_files.all()
        except Exception as e:
            log.warning(f"Unable to retrieve related files for url '{url}': {e}")
            return JsonResponse(
                {
                    "error": "No related files",
                    "files": [],
                    "url": url,
                }
            )

        file_data = [
            {
                "url": related_file.file.url,
                "description": related_file.description,
                "type": related_file.type,
            }
            for related_file in related_files
        ]

        return JsonResponse(
            {
                "url": url,
                "files": file_data,
            }
        )
