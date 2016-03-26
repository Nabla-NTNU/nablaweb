# -*- coding: utf-8 -*-

from .models import MeetingRecord
from django.contrib import admin
from content.admin import ContentAdmin


@admin.register(MeetingRecord)
class MeetingRecordAdmin(ContentAdmin):
    fields = ("picture",
              "cropping",
              "headline",
              "slug",
              "lead_paragraph",
              "body",
              "priority",
              "pub_date",
              "file")
    prepopulated_fields = {"slug": ("headline",)}

