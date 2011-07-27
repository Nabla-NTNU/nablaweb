# -*- coding: utf-8 -*-


from nablaweb.content.views import ContentListView, ContentDetailView, ContentDeleteView
from nablaweb.news.models import News


class NewsListView(ContentListView):
    model = News


class NewsDetailView(ContentDetailView):
    model = News


class NewsDeleteView(ContentDeleteView):
    model = News
