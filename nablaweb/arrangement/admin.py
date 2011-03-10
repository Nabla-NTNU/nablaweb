# arrangement/admin.py

from django.contrib import admin
from arrangement.models import Event

class EventAdmin(admin.ModelAdmin):
    pass

admin.site.register(Event)
