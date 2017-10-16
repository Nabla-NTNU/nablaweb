from image_cropping import ImageCroppingMixin
from django.contrib import admin

from nablapps.nabladet.models import Nablad


@admin.register(Nablad)
class NabladAdmin(ImageCroppingMixin, admin.ModelAdmin):
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
    )
    prepopulated_fields = {"slug": ("headline",)}
