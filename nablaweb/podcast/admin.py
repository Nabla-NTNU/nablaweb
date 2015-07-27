# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Podcast, Season
from image_cropping import ImageCroppingMixin


class PodcastAdmin(ImageCroppingMixin, admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['image', 'cropping', 'title', 'season', 'description', 'is_clip', 'file']
        })
    ]


admin.site.register(Podcast, PodcastAdmin)
admin.site.register(Season)
