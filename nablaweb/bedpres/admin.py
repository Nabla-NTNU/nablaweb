from django.contrib import admin
from bedpres.models import BedPres

class BedPresAdmin(admin.ModelAdmin):
    pass

admin.site.register(BedPres)
