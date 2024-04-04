"""
Admin interface for nabladet app
"""

from django.contrib import admin

from image_cropping import ImageCroppingMixin

from nablapps.news.admin import add_to_frontpage

from .models import Nablad


@admin.register(Nablad)
class NabladAdmin(ImageCroppingMixin, admin.ModelAdmin):
    """Admin interface for Nablad model"""

    fields = (
        "is_public",
        "picture",
        "cropping",
        "headline",
        "slug",
        "lead_paragraph",
        "body",
        "pub_date",
        "file",
        "file_nsfw",
    )
    prepopulated_fields = {"slug": ("headline",)}
    actions = [add_to_frontpage]
