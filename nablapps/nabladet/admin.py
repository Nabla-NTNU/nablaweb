from content.admin import ContentAdmin
from django.contrib import admin

from nablapps.nabladet.models import Nablad


class NabladAdmin(ContentAdmin):
    fields = ("published",
              "is_public",
              "picture",
              "cropping",
              "headline",
              "slug",
              "lead_paragraph",
              "body",
              "priority",
              "pub_date",
              "file")
    prepopulated_fields = {"slug": ("headline",)}


admin.site.register(Nablad, NabladAdmin)
