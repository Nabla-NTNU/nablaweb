"""
Admin for ContentImage
"""
from django.contrib import admin

from .models import ContentImage


@admin.register(ContentImage)
class ContentImageAdmin(admin.ModelAdmin):
    """Admin interface for ContentImage"""

    list_display = ["id", "file", "image_thumb"]
