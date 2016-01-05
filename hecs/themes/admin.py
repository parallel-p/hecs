from django.contrib import admin
from .models import *

admin.site.register(Theme)
admin.site.register(ReferenceGroup)
admin.site.register(ReferenceTarget)
admin.site.register(Reference)
admin.site.register(Blank)
admin.site.register(Comment)