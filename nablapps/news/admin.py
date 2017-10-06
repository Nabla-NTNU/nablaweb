from django.contrib import admin

from image_cropping import ImageCroppingMixin
from content.admin import ChangedByMixin

from .models import News, NewsArticle


@admin.register(News)
class NewsAdmin(ImageCroppingMixin, ChangedByMixin, admin.ModelAdmin):
    fields = ("publication_date",
              "published",
              "picture",
              "cropping",
              "headline",
              "slug",
              "lead_paragraph",
              "body",
              )
    prepopulated_fields = {"slug": ("headline",)}


@admin.register(NewsArticle)
class NewsArticleAdmin(ImageCroppingMixin, ChangedByMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("headline", )}
