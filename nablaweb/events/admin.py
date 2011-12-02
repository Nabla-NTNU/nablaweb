from django.contrib import admin
from events.models import Event, EventRegistration, EventPenalty

class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    fields = ('user', 'number')

class EventAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'registration_required']
    date_hierarchy = 'event_start'
    ordering = ['-event_start']
    search_fields = ['headline', 'body']
    list_filter = ['event_start', 'organizer', 'location']
    inlines = [EventRegistrationInline]
    actions_on_top = True


class EventRegistrationAdmin(admin.ModelAdmin):
    pass

class EventPenaltyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Event, EventAdmin)
admin.site.register(EventRegistration)
admin.site.register(EventPenalty)
