# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.edit import CreateView
from quotes.models import Quote

urlpatterns = patterns('quotes.views',
    url(r'^$', ListAllQuotes.as_view(), name='jobs_list'),
    (r'^legg-til', CreateView.as_view(
        model=Quote
    )),
)

