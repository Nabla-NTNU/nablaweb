# arrangement/admin.py

from django.contrib import admin
from arrangement.models import Arrangement

class ArrangementAdmin(admin.ModelAdmin):
    pass

admin.site.register(Arrangement)
