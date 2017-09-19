# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.forms.widgets import ClearableFileInput, FileInput

from image_cropping import ImageCroppingMixin

from content.models.news import News
from content.forms import NewsForm

from .mixins import ChangedByMixin


class ContentAdmin(ImageCroppingMixin, ChangedByMixin, admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {"widget": ClearableFileInput},
        models.FileField: {"widget": FileInput}
    }
    readonly_fields = ["view_counter"]


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



admin.site.register(News, NewsAdmin)
