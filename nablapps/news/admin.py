from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html

from image_cropping import ImageCroppingMixin
from content.admin import ChangedByMixin

from .models import FrontPageNews, NewsArticle


@admin.register(FrontPageNews)
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
        "title_override",
        "text_override",
        "picture_override",
        "cropping_override",
        "sticky",
        "visible",
        "content_type",
        "object_id",
    )
    actions = [
        "bump",
        "stick", "unstick",
        "hide", "reveal",
    ]

    def content_object_with_link(self, news):
        url = news.get_absolute_url()
        return format_html(
            '{content_type}: <a href="{url}">{news}</a>',
            url=url, news=news,
            content_type=str(news.content_type).capitalize()
        )

    def bump(self, request, queryset):
        for news in queryset:
            news.bump()

    def stick(self, request, queryset):
        queryset.update(sticky=True)

    def unstick(self, request, queryset):
        queryset.update(sticky=False)

    def hide(self, request, queryset):
        queryset.update(visible=False)

    def reveal(self, request, queryset):
        queryset.update(visible=True)


def add_to_frontpage(modeladmin, request, queryset):
    """
    Admin action for models addable to the front page.
    """
    for obj in queryset:
        FrontPageNews.objects.get_or_create(
            object_id=obj.id,
            content_type=ContentType.objects.get_for_model(obj.__class__),
        )


@admin.register(NewsArticle)
class NewsArticleAdmin(ImageCroppingMixin, ChangedByMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("headline", )}
    actions = [add_to_frontpage]
