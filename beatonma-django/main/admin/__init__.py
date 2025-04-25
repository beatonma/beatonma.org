from common.admin import register_model_to_default_admin
from django.conf import settings

from ..models import SiteHCard
from .flatpages import *
from .models import *

admin.site.site_header = settings.SITE_NAME
admin.site.site_title = settings.SITE_NAME
admin.site.index_title = "Index"


register_model_to_default_admin(
    SiteHCard,
    editable_fields=["*"],
    inlines=[
        LinkInline,
    ],
)
