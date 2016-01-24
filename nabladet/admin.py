from nabladet.models import Nablad
from django.contrib import admin
from content.admin import ContentAdmin


class NabladAdmin(ContentAdmin):
    fields = ("published",
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
