"""
Urls for jobs app
"""

from django.urls import path, re_path

from .feeds import RecentJobs
from .views import (
    CompanyList,
    EverythingList,
    MonthList,
    RelevantForLinjeList,
    RelevantForYearList,
    ShowJob,
    TagList,
    YearList,
)

urlpatterns = [
    path(
        "dato/<int:year>/", YearList.as_view(), name="jobs_year_list"
    ),  # Stillingsannonser som er lagt inn dette året
    path(
        "dato/<int:year>/<int:month>/",
        MonthList.as_view(),
        name="jobs_month_list",
    ),  # Stillingsannonser som er lagt inn denne måneden
    re_path(
        r"^bedrift/(?P<pk>\d{1,8})-(?P<slug>[-\w]*)$",
        CompanyList.as_view(),
        name="company_detail",
    ),  # Stillingsannonser fra én bedrift
    path(
        "linje/<str:linje>/",
        RelevantForLinjeList.as_view(),
        name="relevant_for_linje_list",
    ),
    path(
        "kull/<int:year>/",
        RelevantForYearList.as_view(),
        name="relevant_for_year_list",
    ),
    path("tag/<str:tag>/", TagList.as_view(), name="tag_list"),
    path("", EverythingList.as_view(), name="jobs_list"),
    path("<int:pk>/<str:slug>/", ShowJob.as_view(), name="advert_detail"),
    path("feed/", RecentJobs()),
]
