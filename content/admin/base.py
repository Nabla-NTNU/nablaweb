# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from image_cropping import ImageCroppingMixin
from filebrowser.widgets import ClearableFileInput, FileInput
from django.db import models
from .config import ConfigurationModelAdmin

from content.models.news import News
from content.models.events import Event, EventRegistration
from content.forms import NewsForm, EventForm
from content.models.album import Album, AlbumImage
from content.models.blog import Blog, BlogPost
from content.models.base import ContentImage
from content.models.splash import SplashConfig


class ChangedByMixin(object):
    def save_model(self, request, obj, form, change):
        obj.last_changed_by = request.user

        # Update created_by
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        super(ChangedByMixin, self).save_model(request, obj, form, change)


class ListenMixin(object):
    """
    Assumes the form has a boolean field 'listen'.
    """

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('listen'):
            user = request.user
            obj.edit_listeners.add(user)
        elif obj.id:
            user = request.user
            obj.edit_listeners.remove(user)

        super(ListenMixin, self).save_model(request, obj, form, change)


class ContentAdmin(ListenMixin, ImageCroppingMixin, ChangedByMixin, admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {"widget": ClearableFileInput},
        models.FileField: {"widget": FileInput}
    }
    readonly_fields = ["view_counter"]


class BlogPostAdmin(ListenMixin, ChangedByMixin, admin.ModelAdmin):
    readonly_fields = ["view_counter"]
    ordering = ['-created_date']


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
              "edit_listeners")
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
              "edit_listeners")
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
admin.site.register(Blog)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(SplashConfig, ConfigurationModelAdmin)
