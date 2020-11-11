from django.contrib import admin

from image_cropping import ImageCroppingMixin

from .models import Podcast, Season


class PodcastAdmin(ImageCroppingMixin, admin.ModelAdmin):
    fields = (
        "image",
        "cropping",
        "title",
        "season",
        "description",
        "short_title",
        "has_video",
        "is_clip",
        "file",
        "pub_date",
    )
    list_display = ("title", "pub_date", "season", "is_clip", "has_video")
    list_filter = ["pub_date"]


admin.site.register(Podcast, PodcastAdmin)
admin.site.register(Season)
