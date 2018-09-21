"""
Urls for blog app
"""
from django.conf.urls import url
from .views import (
    BlogListView,
    BlogPostView,
    BlogView,
)

urlpatterns = [
    url(r'^$',
        BlogListView.as_view(),
        name="blog"),
    url(r'^(?P<blog>[\w-]+)/$',
        BlogView.as_view(),
        name="blog"),
    url(r'^(?P<blog>[\w-]+)/(?P<slug>[\w-]+)$',
        BlogPostView.as_view(),
        name="blog_post"),
]
