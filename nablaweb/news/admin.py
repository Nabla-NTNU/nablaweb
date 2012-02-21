from news.models import News
from django.contrib import admin
from news.forms import NewsForm
from content.admin import ContentAdmin


class NewsAdmin(ContentAdmin):
    form = NewsForm


admin.site.register(News, NewsAdmin)
