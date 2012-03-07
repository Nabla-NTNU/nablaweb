from news.models import News
from django.contrib import admin
from news.forms import NewsForm
from content.admin import ContentAdmin


class NewsAdmin(ContentAdmin):
    form = NewsForm
    fields = ("picture",
              "cropping",
              "headline",
              "slug",
              "lead_paragraph",
              "body")
    prepopulated_fields = {"slug": ("headline",)}


admin.site.register(News, NewsAdmin)
