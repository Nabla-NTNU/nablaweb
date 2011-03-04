# arrangement/admin.py

from django.contrib import admin
from arrangement.models import SimpleEvent, Event

class SimpleEventAdmin(admin.ModelAdmin):
    pass

class EventAdmin(admin.ModelAdmin):
    pass

admin.site.register(SimpleEvent)
admin.site.register(Event)
