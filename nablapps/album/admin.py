"""
Admin interface for album app
"""
from django.contrib import admin

from nablapps.core.admin import ChangedByMixin

from .models import Album, AlbumForm, AlbumImage


class AlbumImageInline(admin.TabularInline):
    """Inline album image"""

    model = AlbumImage
    fk_name = "album"
    fields = ("num", "file", "description", "is_display_image")
    readonly_fields = (
        "num",
        "image_thumb",
    )
    ordering = ("num",)
    extra = 0


@admin.register(Album)
class AlbumAdmin(ChangedByMixin, admin.ModelAdmin):
    """Admin interface for Album model"""

    list_display = [
        "__str__",
        "visibility",
        "created_by",
        "created_date",
        # "image_thumb",
        "parent",
    ]
    form = AlbumForm
    inlines = [AlbumImageInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.save_photos(form.instance)

    def response_add(self, request, obj, post_url_continue=None):
        obj = self.after_saving_model_and_related_inlines(obj)
        return super().response_add(request, obj)

    def response_change(self, request, obj):
        obj = self.after_saving_model_and_related_inlines(obj)
        return super().response_change(request, obj)

    def after_saving_model_and_related_inlines(self, obj):
        images = AlbumImage.objects.filter(album=obj.pk)

        # give images the correct number
        i = 0
        for img in images:
            img.num = i
            img.save()
            i = i + 1
        return obj

    def image_thumb(self, album):
        """Return html for displaying thumbnail of album"""
        return album.first and album.first.image_thumb()

    image_thumb.allow_tags = True
