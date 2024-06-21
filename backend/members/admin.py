from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Proposed)
admin.site.register(Accepted)
admin.site.register(Rejected)