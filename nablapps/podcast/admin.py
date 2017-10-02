from django.contrib import admin
from image_cropping import ImageCroppingMixin
from .models import Podcast, Season


class PodcastAdmin(ImageCroppingMixin, admin.ModelAdmin):
    fields = (
        "publication_date",
        "published",
        'image',
        'cropping',
        'title',
        'season',
        'description',
        'extra_markdown',
        'is_clip',
        'file',
        'pub_date',
    )
    list_display = ('title', 'pub_date', 'season', 'is_clip')
    list_filter = ['pub_date']


admin.site.register(Podcast, PodcastAdmin)
admin.site.register(Season)
