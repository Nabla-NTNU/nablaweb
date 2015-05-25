# -*- coding: utf-8 -*-

from django.contrib import admin
from podcast.models import Podcast
from image_cropping import ImageCroppingMixin


class PodcastAdmin(ImageCroppingMixin, admin.ModelAdmin):
    fieldsets = [
        (None, {
        'fields': ['image', 'cropping', 'title', 'description', 'file']
        })
    ]

admin.site.register(Podcast, PodcastAdmin)
