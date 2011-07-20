# -*- coding: utf-8 -*-


from nablaweb.content.views import ContentUpdateView
from nablaweb.news.models import News
from nablaweb.news.forms import NewsForm


class NewsUpdateView(ContentUpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news/news_form.html'
    form_base = 'news/news_form_base.html'
    success_detail = 'news_detail'
