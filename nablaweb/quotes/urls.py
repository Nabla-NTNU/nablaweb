# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.edit import CreateView
from quotes.models import Quote

urlpatterns = patterns('quotes.views',
    (r'^legg-til', CreateView.as_view(
        model=Quote
    )),
)

