# -*- coding: utf-8 -*-
from django.contrib import admin
from image_cropping import ImageCroppingMixin
from .models import Album, AlbumImage


class ChangedByMixin(object):
    def save_model(self, request, obj, form, change):
        obj.last_changed_by = request.user

        # Hvis objekter ikke er laget av noen, legg til denne brukeren
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        super(ChangedByMixin, self).save_model(request, obj, form, change)


class ContentAdmin(ImageCroppingMixin, ChangedByMixin, admin.ModelAdmin):
    pass


class AlbumAdmin(admin.ModelAdmin):
    pass


admin.site.register(Album, AlbumAdmin)
admin.site.register(AlbumImage)
