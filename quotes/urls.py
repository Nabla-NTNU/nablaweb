# -*- coding: utf-8 -*-
from django.conf.urls import *
from django.views.generic.edit import CreateView
from quotes.views import *

urlpatterns = patterns('quotes.views',
    url(r'^$', ListAllQuotes.as_view(), name='quote_list'),
    (r'^legg-til', CreateView.as_view(
        model=Quote
    )),
)

