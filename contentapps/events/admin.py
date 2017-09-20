from django.contrib import admin
from content.admin import ContentAdmin
from .forms import EventForm
from .models import Event, EventRegistration

admin.site.register(EventRegistration)


@admin.register(Event)
class EventAdmin(ContentAdmin):
    fields = ("publication_date",
              "published",
              "picture",
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
              "open_for",
              "facebook_url",
              )
    form = EventForm
    list_display = ['__str__', 'registration_required']
    date_hierarchy = 'event_start'
    ordering = ['-event_start']
    search_fields = ['headline', 'body']
    list_filter = ['event_start', 'organizer', 'location']
    actions_on_top = True
