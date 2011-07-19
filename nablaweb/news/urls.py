from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from nablaweb.news.models import News

urlpatterns = patterns('news.views',

    # Administrasjon
    (r'^opprett/$', 'create_or_edit_news'),
    (r'^(?P<news_id>\d{1,8})/endre/$', 'create_or_edit_news'),

    # Offentlig
    (r'^$',
     ListView.as_view(model=News,
                      queryset=New.objects.all().order_by('-created_date')[:5],
                      context_object_name='content_list',)),
    (r'^(?P<pk>\d{1,8})/$',
     DetailView.as_view(model=News,
                        context_object_name='content',)),
)
