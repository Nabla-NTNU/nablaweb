# -*- coding: utf-8 -*-

# URL-er for stillingsannonser-appen

from django.conf.urls.defaults import *
from jobs.views import *

urlpatterns = patterns('',
    (r'^$', EverythingList.as_view()),
    #(r'^stillinger/(?P<year>\d{4})/$', 'jobs.views.datelist'),
    #(r'^stillinger/(?P<year>\d{4})/(?P<month>\d{2})/$', 'jobs.views.datelist'),
    #(r'^stillinger/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'jobs.views.datelist'),
    (r'^(?P<company>\D{1,25})/$', CompanyList.as_view()),
    #(r'^stillinger/(?P<company>\D{})/(?P<jobid>\d{3}/$)', 'jobs.views.jobview')
)
