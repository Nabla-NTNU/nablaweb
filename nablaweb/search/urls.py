from django.conf.urls.defaults import *
from haystack.forms import HighlightedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView
from haystack.views import SearchView, search_view_factory
from nablaweb.search.forms import NewSearchForm

urlpatterns = patterns('haystack.views',
    url(r'^$', search_view_factory(view_class = SearchView, form_class = NewSearchForm), name='haystack_search'),
)
