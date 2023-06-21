from django.contrib import admin

from .flatpages import *
from .models import *

admin.site.site_header = "beatonma.org"
admin.site.index_title = "Index"
admin.site.site_title = "beatonma.org"
