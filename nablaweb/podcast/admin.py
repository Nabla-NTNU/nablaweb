# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Podcast, Season
from image_cropping import ImageCroppingMixin


class PodcastAdmin(ImageCroppingMixin, admin.ModelAdmin):
    fields = ['image', 'cropping', 'title', 'season', 'description', 'is_clip', 'file', 'pub_date']
    list_display = ('title', 'pub_date', 'season', 'is_clip')
    list_filter = ['pub_date']


admin.site.register(Podcast, PodcastAdmin)
admin.site.register(Season)
