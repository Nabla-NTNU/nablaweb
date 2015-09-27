from django.conf.urls import url
from haystack.views import SearchView, search_view_factory
from .forms import NewSearchForm


urlpatterns = [
    url(r'^$', search_view_factory(view_class=SearchView,
                                   form_class=NewSearchForm),
        name='haystack_search'),
]
