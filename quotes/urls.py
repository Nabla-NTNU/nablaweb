# -*- coding: utf-8 -*-
from django.conf.urls import *
from django.views.generic.edit import CreateView
from .views import *

urlpatterns = [
    url(r'^$', ListAllQuotes.as_view(), name='quote_list'),
    url(r'^legg-til', CreateView.as_view(model=Quote)),
]

