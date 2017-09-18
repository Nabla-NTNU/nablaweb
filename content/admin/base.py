# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.forms.widgets import ClearableFileInput, FileInput

from image_cropping import ImageCroppingMixin

from content.models.news import News
from content.models.events import Event, EventRegistration
from content.forms import NewsForm, EventForm
from content.models.album import Album, AlbumImage
from content.models.base import ContentImage

from .mixins import ChangedByMixin


class ContentAdmin(ImageCroppingMixin, ChangedByMixin, admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {"widget": ClearableFileInput},
        models.FileField: {"widget": FileInput}
    }
    readonly_fields = ["view_counter"]


class AlbumImageInline(admin.TabularInline):
    model = AlbumImage
    fk_name = "album"
    fields = ('num', 'file', 'description', 'image_thumb')
    readonly_fields = ('image_thumb',)
    ordering = ('num',)


class AlbumAdmin(ChangedByMixin, admin.ModelAdmin):
    list_display = ['__str__', 'visibility', 'created_by', 'created_date', 'image_thumb']
    inlines = [AlbumImageInline]

    def image_thumb(self, album):
        if album.first:
            return album.first.image_thumb()

    image_thumb.allow_tags = True


class EventAdmin(ContentAdmin):
    fields = ("publication_date",
              "published",
              "picture",
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
              "facebook_url",
              )
    form = EventForm
    list_display = ['__unicode__', 'registration_required']
    date_hierarchy = 'event_start'
    ordering = ['-event_start']
    search_fields = ['headline', 'body']
    list_filter = ['event_start', 'organizer', 'location']
    actions_on_top = True


class NewsAdmin(ContentAdmin):
    form = NewsForm
    fields = ("publication_date",
              "published",
              "picture",
              "cropping",
              "headline",
              "slug",
              "lead_paragraph",
              "body",
              "priority",
              "allow_comments",
              )
    prepopulated_fields = {"slug": ("headline",)}

    def get_queryset(self, request):
        this_type = ContentType.objects.get_for_model(News)
        qs = super(NewsAdmin, self).get_queryset(request)
        return qs.filter(content_type=this_type)


class ContentImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'image_thumb']


admin.site.register(Album, AlbumAdmin)
admin.site.register(ContentImage, ContentImageAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventRegistration)
admin.site.register(News, NewsAdmin)
