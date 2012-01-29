from news.models import News
from django.contrib import admin


class NewsAdmin(admin.ModelAdmin):
    form = NewsForm


admin.site.register(News, NewsAdmin)
