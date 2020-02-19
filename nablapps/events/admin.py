"""Admin for events app"""
from django.contrib import admin

from image_cropping import ImageCroppingMixin

from nablapps.core.admin import ChangedByMixin
from nablapps.news.admin import add_to_frontpage

from .forms import EventForm
from .models import Event, EventRegistration


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    """Admin interface for eventregistration model"""

    search_fields = [
        "user__username",
        "user__first_name",
        "user__last_name",
        "event__headline",
    ]
    ordering = ["-event__event_start"]


@admin.register(Event)
class EventAdmin(ImageCroppingMixin, ChangedByMixin, admin.ModelAdmin):
    """Admin interface for Event model"""

    fields = (
        "picture",
        "cropping",
        "headline",
        "slug",
        "short_name",
        "lead_paragraph",
        "body",
        "is_bedpres",
        "company",
        "organizer",
        "location",
        "event_start",
        "event_end",
        "registration_required",
        "penalty",
        "registration_deadline",
        "registration_start",
        "deregistration_deadline",
        "places",
        "has_queue",
        "open_for",
        "facebook_url",
    )
    filter_horizontal = ("open_for",)
    form = EventForm
    list_display = ["__str__", "registration_required"]
    date_hierarchy = "event_start"
    ordering = ["-event_start"]
    search_fields = ["headline", "body"]
    list_filter = ["event_start", "organizer", "location"]
    actions_on_top = True
    actions = [add_to_frontpage]
