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
    readonly_fields = ('image_thumb',)
    ordering = ('num',)


@admin.register(Album)
class AlbumAdmin(ChangedByMixin, admin.ModelAdmin):
    """Admin interface for Album model"""
    list_display = ['__str__', 'visibility', 'created_by', 'created_date', 'image_thumb']
    inlines = [AlbumImageInline]

    def image_thumb(self, album):
        """Return html for displaying thumbnail of album"""
        return album.first and album.first.image_thumb()

    image_thumb.allow_tags = True
