# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from content.admin import ContentAdmin
from .forms import EventForm
from .models import Event, EventRegistration


class EventAdmin(ContentAdmin):
    fields = ("picture",
              "cropping",
              "headline",
              "slug",
              "short_name",
              "lead_paragraph",
              "body",
              "priority",
              "organizer",
              "location",
              "event_start",
              "event_end",
              "registration_required",
              "registration_deadline",
              "registration_start",
              "deregistration_deadline",
              "places",
              "has_queue",
              "allow_comments",
              "open_for",
              "facebook_url")
    form = EventForm
    list_display = ['__unicode__', 'registration_required']
    date_hierarchy = 'event_start'
    ordering = ['-event_start']
    search_fields = ['headline', 'body']
    list_filter = ['event_start', 'organizer', 'location']
    actions_on_top = True


admin.site.register(Event, EventAdmin)
admin.site.register(EventRegistration)
