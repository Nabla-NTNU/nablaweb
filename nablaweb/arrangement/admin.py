# arrangement/admin.py

from django.contrib import admin
from arrangement.models import Event, EventRegistration, EventPenalty

class EventAdmin(admin.ModelAdmin):
    pass

class EventRegistrationAdmin(admin.ModelAdmin):
    pass

class EventPenaltyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Event)
admin.site.register(EventRegistration)
admin.site.register(EventPenalty)
