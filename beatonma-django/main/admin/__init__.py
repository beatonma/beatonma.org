from django.conf import settings
from django.contrib import admin

from .flatpages import *
from .models import *

admin.site.site_header = settings.SITE_NAME
admin.site.site_title = settings.SITE_NAME
admin.site.index_title = "Index"
