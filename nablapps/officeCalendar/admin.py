from django.contrib import admin, messages
from .models import OfficeEvent

from django.db import models
from django import forms

@admin.register(OfficeEvent)
class OfiiceEventAdmin(admin.ModelAdmin):
    """Admin interface for OfficeEvent"""
    formfield_overrides = {
        models.TimeField: {'widget': forms.TimeInput(attrs={ 'type': 'time' }) }
    }

    def save_model(self, request, obj, form, change):
        if obj.check_overlap().exists():
            messages.warning(request,
                             "Dette eventet overlapper med et annet event! Ditt event ble reservert,\
                             men vær bevisst på at det nå er flere reservasjoner for det tidsrommet.")
        super().save_model(request, obj, form, change)
