# -*- coding: utf-8 -*-

from django.contrib import admin
from podcast.models import Podcast

class PodcastAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
        'fields': ['title', 'description', 'file']
        })
    ]

admin.site.register(Podcast, PodcastAdmin)
