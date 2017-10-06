from django.contrib import admin
from django.utils.html import format_html

from image_cropping import ImageCroppingMixin
from content.admin import ChangedByMixin

from .models import News, NewsArticle


@admin.register(News)
class NewsAdmin(ImageCroppingMixin, ChangedByMixin, admin.ModelAdmin):
    date_hierarchy = "bump_time"
    list_display = (
        "headline",
        "content_object_with_link",
        "sticky",
        "visible",
        "bump_time",
        "created_date",
    )
    fields = (
        "headline",
        "lead_paragraph",
        "picture",
        "cropping",
        "sticky",
        "visible",
        "content_type",
        "object_id",
    )

    def content_object_with_link(self, obj):
        url = obj.content_object.get_absolute_url()
        return format_html(
            '{content_type}: <a href="{url}">{obj}</a>',
            url=url, obj=obj,
            content_type=str(obj.content_type).capitalize()
        )


@admin.register(NewsArticle)
class NewsArticleAdmin(ImageCroppingMixin, ChangedByMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("headline", )}
