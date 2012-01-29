from django.contrib import admin
from events.forms import EventForm
from events.models import Event, EventRegistration, EventPenalty
from news.admin import NewsAdmin


class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    fields = ('user', 'number')


class EventAdmin(NewsAdmin):
    form = EventForm
    list_display = ['__unicode__', 'registration_required']
    date_hierarchy = 'event_start'
    ordering = ['-event_start']
    search_fields = ['headline', 'body']
    list_filter = ['event_start', 'organizer', 'location']
    inlines = [EventRegistrationInline]
    actions_on_top = True


admin.site.register(Event, EventAdmin)
admin.site.register(EventRegistration)
admin.site.register(EventPenalty)
