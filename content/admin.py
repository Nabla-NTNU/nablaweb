# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from image_cropping import ImageCroppingMixin
from filebrowser.widgets import ClearableFileInput, FileInput
from django.db import models

from content.models.news import News
from .forms import EventForm
from content.models.events import Event, EventRegistration
from content.forms import NewsForm
from content.models.album import Album, AlbumImage
from content.widgets import MultipleImagesChooser


class ChangedByMixin(object):
    def save_model(self, request, obj, form, change):
        obj.last_changed_by = request.user

        # Hvis objekter ikke er laget av noen, legg til denne brukeren
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        super(ChangedByMixin, self).save_model(request, obj, form, change)


class ContentAdmin(ImageCroppingMixin, ChangedByMixin, admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {"widget": ClearableFileInput},
        models.FileField: {"widget": FileInput}
    }


class AlbumAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {"widget": MultipleImagesChooser}
    }


class EventAdmin(ContentAdmin):
    fields = ("picture",
              "cropping",
              "headline",
              "slug",
              "short_name",
              "lead_paragraph",
              "body",
              "priority",
              "organizer",
              "location",
              "event_start",
              "event_end",
              "registration_required",
              "registration_deadline",
              "registration_start",
              "deregistration_deadline",
              "places",
              "has_queue",
              "allow_comments",
              "open_for",
              "facebook_url")
    form = EventForm
    list_display = ['__unicode__', 'registration_required']
    date_hierarchy = 'event_start'
    ordering = ['-event_start']
    search_fields = ['headline', 'body']
    list_filter = ['event_start', 'organizer', 'location']
    actions_on_top = True


class NewsAdmin(ContentAdmin):
    form = NewsForm
    fields = ("picture",
              "cropping",
              "headline",
              "slug",
              "lead_paragraph",
              "body",
              "priority",
              "allow_comments")
    prepopulated_fields = {"slug": ("headline",)}

    def get_queryset(self, request):
        this_type = ContentType.objects.get_for_model(News)
        qs = super(NewsAdmin, self).get_queryset(request)
        return qs.filter(content_type=this_type)


admin.site.register(Album, AlbumAdmin)
admin.site.register(AlbumImage)
admin.site.register(Event, EventAdmin)
admin.site.register(EventRegistration)
admin.site.register(News, NewsAdmin)
