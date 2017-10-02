from content.admin import ChangedByMixin
from django.contrib import admin
from .models import MeetingRecord


@admin.register(MeetingRecord)
class MeetingRecordAdmin(ChangedByMixin, admin.ModelAdmin):
    fields = (
        "title",
        "slug",
        "description",
        "pub_date",
        "file")
    prepopulated_fields = {"slug": ("title",)}
