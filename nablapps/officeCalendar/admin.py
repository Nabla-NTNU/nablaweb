from django.contrib import admin
from .models import OfficeEvent

from django.db import models
from django import forms

@admin.register(OfficeEvent)
class OfiiceEventAdmin(admin.ModelAdmin):
    """Admin interface for OfficeEvent"""
    formfield_overrides = {
        models.DurationField: {'widget': forms.TimeInput(attrs={ 'type': 'time' }) }
    }
