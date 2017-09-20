from django.contrib import admin
from content.admin import ChangedByMixin
from .models import Album, AlbumImage


class AlbumImageInline(admin.TabularInline):
    model = AlbumImage
    fk_name = "album"
    fields = ('num', 'file', 'description', 'image_thumb')
    readonly_fields = ('image_thumb',)
    ordering = ('num',)


@admin.register(Album)
class AlbumAdmin(ChangedByMixin, admin.ModelAdmin):
    list_display = ['__str__', 'visibility', 'created_by', 'created_date', 'image_thumb']
    inlines = [AlbumImageInline]

    def image_thumb(self, album):
        if album.first:
            return album.first.image_thumb()

    image_thumb.allow_tags = True
