# arrangement/admin.py

from django.contrib import admin
from arrangement.models import Event, NoShowDot

class EventAdmin(admin.ModelAdmin):
    pass

class NoShowDotAdmin(admin.ModelAdmin):
    pass

admin.site.register(Event)
admin.site.register(NoShowDot)
