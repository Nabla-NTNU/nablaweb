# -*- coding: utf-8 -*-

from django.contrib import admin
from content.admin import ContentAdmin
from podcast.models import Podcast

class PodcastAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
        'fields': ['title', 'description', 'pub_date',  'file']
        })
    ]

admin.site.register(Podcast, PodcastAdmin)
