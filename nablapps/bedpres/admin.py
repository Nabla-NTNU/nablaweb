from django.contrib import admin
from image_cropping import ImageCroppingMixin
from nablapps.news.admin import add_to_frontpage
from .models import BedPres


@admin.register(BedPres)
class BedPresAdmin(ImageCroppingMixin, admin.ModelAdmin):
    fields = (
        "picture",
        "cropping",
        "bpcid",
        "headline",
        "slug",
        "company",
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
        "has_queue",
    )
    prepopulated_fields = {"slug": ("headline",)}
    actions = [add_to_frontpage]
