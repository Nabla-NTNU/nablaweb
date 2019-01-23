"""
Admin interface for album app
"""
from django.contrib import admin
from content.admin import ChangedByMixin
from .models import Album, AlbumImage


class AlbumImageInline(admin.TabularInline):
    """Inline album image"""
    model = AlbumImage
    fk_name = "album"
    fields = ('num', 'file', 'description', 'image_thumb')
    readonly_fields = ('num', 'image_thumb',)
    ordering = ('num',)


@admin.register(Album)
class AlbumAdmin(ChangedByMixin, admin.ModelAdmin):
    """Admin interface for Album model"""
    list_display = ['__str__', 'visibility', 'created_by', 'created_date', 'image_thumb']
    inlines = [AlbumImageInline]

    def response_add(self, request, new_object):
        obj = self.after_saving_model_and_related_inlines(new_object)
        return super().response_add(request, obj)

    def response_change(self, request, obj):
        obj = self.after_saving_model_and_related_inlines(obj)
        return super().response_change(request, obj)

    def after_saving_model_and_related_inlines(self, obj):

        images = AlbumImage.objects.filter(album=obj.pk)

        i = 1
        for img in images:
            img.num = i
            img.save()
            i = i + 1
        return obj

    def image_thumb(self, album):
        """Return html for displaying thumbnail of album"""
        return album.first and album.first.image_thumb()

    image_thumb.allow_tags = True
