"""
Admin interface for meeting record app
"""
from content.admin import ChangedByMixin
from django.contrib import admin
from .models import MeetingRecord


@admin.register(MeetingRecord)
class MeetingRecordAdmin(ChangedByMixin, admin.ModelAdmin):
    """Admin interface for MeetingRecord model"""
    fields = (
        "title",
        "slug",
        "description",
        "pub_date",
        "file")
    prepopulated_fields = {"slug": ("title",)}
