from news.models import News
from django.contrib import admin
from news.forms import NewsForm


class NewsAdmin(admin.ModelAdmin):
    form = NewsForm


admin.site.register(News, NewsAdmin)
