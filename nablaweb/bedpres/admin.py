from django.contrib import admin
from events.admin import EventAdmin
from bedpres.models import BedPres


class BedPresAdmin(EventAdmin):
    form = BedPresForm


admin.site.register(BedPres, BedPresAdmin)
