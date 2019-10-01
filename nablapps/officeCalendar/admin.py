from django.contrib import admin, messages
from .models import OfficeEvent

from django.db import models
from django import forms

@admin.register(OfficeEvent)
class OfiiceEventAdmin(admin.ModelAdmin):
    """Admin interface for OfficeEvent"""
    def get_changeform_initial_data(self, request):
        return {'contact_person': request.user.pk}

    def save_model(self, request, obj, form, change):
        if obj.check_overlap().exists():
            messages.warning(request,
                             "Dette eventet overlapper med et annet event! Ditt event ble reservert,\
                             men vær bevisst på at det nå er flere reservasjoner for det tidsrommet.")
        super().save_model(request, obj, form, change)
