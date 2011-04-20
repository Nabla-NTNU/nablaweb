# arrangement/admin.py

from django.contrib import admin
from arrangement.models import Event, EventRegistration, NoShowDot

class EventAdmin(admin.ModelAdmin):
    pass

class EventRegistrationAdmin(admin.ModelAdmin):
    pass

class NoShowDotAdmin(admin.ModelAdmin):
    pass

admin.site.register(Event)
admin.site.register(EventRegistration)
admin.site.register(NoShowDot)
