# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from events.forms import EventForm
from events.models import Event, EventRegistration, EventPenalty
from news.admin import NewsAdmin


class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    fields = ('user', 'number')


class EventAdmin(NewsAdmin):
    fields = ("picture",
              "cropping",
              "headline",
              "slug",
              "short_name",
              "lead_paragraph",
              "body",
              "organizer",
              "location",
              "event_start",
              "event_end",
              "registration_required",
              "registration_deadline",
              "registration_start",
              "deregistration_deadline",
              "places",
              "has_queue")
    form = EventForm
    list_display = ['__unicode__', 'registration_required']
    date_hierarchy = 'event_start'
    ordering = ['-event_start']
    search_fields = ['headline', 'body']
    list_filter = ['event_start', 'organizer', 'location']
    inlines = [EventRegistrationInline]
    actions_on_top = True

    def queryset(self, request):
        """
        Henter objekter med content_type=Event

        Dette er nødvendig for å ikke inkludere objekter av typen
        BedPres i listen.
        """
        this_type = ContentType.objects.get_for_model(Event)
        # NewsAdmin henter kun News, så superklassen til NewsAdmin må
        # overskrives istedenfor superklassen til EventAdmin
        qs = super(NewsAdmin, self).queryset(request)
        return qs.filter(content_type=this_type)


admin.site.register(Event, EventAdmin)
admin.site.register(EventRegistration)
admin.site.register(EventPenalty)
