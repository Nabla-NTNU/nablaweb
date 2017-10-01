# -*- coding: utf-8 -*-

from .models import MeetingRecord
from django.contrib import admin
from content.admin import ChangedByMixin


@admin.register(MeetingRecord)
class MeetingRecordAdmin(ChangedByMixin, admin.ModelAdmin):
    fields = (
        "title",
        "slug",
        "description",
        "pub_date",
        "file")
    prepopulated_fields = {"slug": ("title",)}
