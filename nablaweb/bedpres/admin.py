from django.contrib import admin
from events.admin import EventAdmin
from bedpres.models import BedPres

class BedPresAdmin(EventAdmin):
    pass

admin.site.register(BedPres, BedPresAdmin)
