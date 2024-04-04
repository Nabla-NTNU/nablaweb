"""
Admin interface for meeting record app
"""

from django.contrib import admin

from nablapps.core.admin import ChangedByMixin

from .models import MeetingRecord


@admin.register(MeetingRecord)
class MeetingRecordAdmin(ChangedByMixin, admin.ModelAdmin):
    """Admin interface for MeetingRecord model"""

    fields = ("title", "slug", "description", "pub_date", "file")
    prepopulated_fields = {"slug": ("title",)}
