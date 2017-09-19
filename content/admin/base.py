from django.contrib import admin
from django.db import models
from django.forms.widgets import ClearableFileInput, FileInput

from image_cropping import ImageCroppingMixin
from .mixins import ChangedByMixin


class ContentAdmin(ImageCroppingMixin, ChangedByMixin, admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {"widget": ClearableFileInput},
        models.FileField: {"widget": FileInput}
    }
    readonly_fields = ["view_counter"]
