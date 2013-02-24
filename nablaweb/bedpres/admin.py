from django.contrib import admin
from content.admin import ContentAdmin
from bedpres.models import BedPres
from bedpres.forms import BedPresForm


class BedPresAdmin(ContentAdmin):
    fields = ("picture",
              "cropping",
              "bpcid",
              "headline",
              "company",
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
    #form = BedPresForm


admin.site.register(BedPres, BedPresAdmin)
