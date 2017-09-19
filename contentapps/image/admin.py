from django.contrib import admin
from .models import ContentImage


@admin.register(ContentImage)
class ContentImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'image_thumb']
