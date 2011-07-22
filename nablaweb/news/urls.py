# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from nablaweb.news.models import News
from nablaweb.news.forms import NewsForm, NewsFormPreview


urlpatterns = patterns('nablaweb.news.views',

    # Administrasjon
    (r'^opprett/$', NewsFormPreview(form=NewsForm)),
    (r'^(?P<pk>\d{1,8})/endre/$', NewsFormPreview(form=NewsForm)),

    # Offentlig
    (r'^$',
     ListView.as_view(model=News,
                      queryset=News.objects.all().order_by('-created_date')[:5],
                      context_object_name='content_list',)),
    url(r'^(?P<pk>\d{1,8})/$',
        DetailView.as_view(model=News,
                           context_object_name='content',),
        name='news_detail',),
)
