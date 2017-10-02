from django.conf.urls import url
from .views import (
    EverythingList,
    CompanyList,
    MonthList,
    RelevantForLinjeList,
    RelevantForYearList,
    ShowJob,
    TagList,
    YearList,
)
from .feeds import RecentJobs

urlpatterns = [
    url(r'^dato/(?P<year>\d{4})/$',
        YearList.as_view(),
        name='jobs_year_list'),  # Stillingsannonser som er lagt inn dette året
    url(r'^dato/(?P<year>\d{4})/(?P<month>\d{2})/$',
        MonthList.as_view(),
        name='jobs_month_list'),  # Stillingsannonser som er lagt inn denne måneden
    url(r'^bedrift/(?P<pk>\d{1,8})-(?P<slug>[-\w]*)$',
        CompanyList.as_view(),
        name='company_detail'),  # Stillingsannonser fra én bedrift
    url(r'^linje/(?P<linje>[-\w\s]{1,50})/$',
        RelevantForLinjeList.as_view(),
        name='relevant_for_linje_list'),
    url(r'^kull/(?P<year>\d{1,5})/$',
        RelevantForYearList.as_view(),
        name='relevant_for_year_list'),
    url(r'^tag/(?P<tag>[-\w ]{1,50})/$',
        TagList.as_view(),
        name='tag_list'),
    url(r'^$',
        EverythingList.as_view(),
        name='jobs_list'),
    url(r'^(?P<pk>\d{1,8})/(?P<slug>[-\w]*)$',
        ShowJob.as_view(),
        name='advert_detail'),
    url(r'^feed/$', RecentJobs()),
]
