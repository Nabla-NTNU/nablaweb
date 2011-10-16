# -*- coding: utf-8 -*-

# URL-er for stillingsannonser-appen

from django.conf.urls.defaults import *
from jobs.views import *

urlpatterns = patterns('',
    (r'^$', EverythingList.as_view()),
    (r'^(?P<year>\d{4})/$', DateList.as_view()),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$', DateList.as_view()),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', DateList.as_view()),
    (r'^(?P<company>\D{1,25})/$', CompanyList.as_view()),
    (r'^(?P<company>\D{})/(?P<jobid>\d{1,5})/$', ShowJob.as_view())
)
