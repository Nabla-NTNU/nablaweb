# -*- coding: utf-8 -*-

# URL-er for stillingsannonser-appen

from django.conf.urls.defaults import *
from jobs.views import *

urlpatterns = patterns('',
    (r'^$', EverythingList.as_view()),
    (r'^dato/(?P<year>\d{4})/$', DateList.as_view()), # Stillingsannonser som er LAGT INN eller LØPER UT i år
    (r'^dato/(?P<year>\d{4})/(?P<month>\d{2})/$', DateList.as_view()), # Stillingsannonser som er LAGT INN eller LØPER UT denne måneden
    (r'^(?P<company>\D{1,25})/$', CompanyList.as_view()),
    (r'^(?P<company>\D{1,25})/(?P<pk>\d{1,5})/$', ShowJob.as_view()),
    (r'^(?P<pk>\d{1,5})/$', RedirectJob.as_view()),
)
