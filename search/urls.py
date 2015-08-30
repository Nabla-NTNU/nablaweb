from django.conf.urls import *
from haystack.views import SearchView, search_view_factory
from search.forms import NewSearchForm

urlpatterns = patterns('haystack.views',
    url(r'^$', search_view_factory(view_class = SearchView, form_class = NewSearchForm), name='haystack_search'),
)
