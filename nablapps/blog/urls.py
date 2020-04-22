"""
Urls for blog app
"""
# from django.conf.urls import url
from django.urls import path

from .views import BlogListView, BlogPostView, BlogView

urlpatterns = [
    path("", BlogListView.as_view(), name="blog"),
    path("<str:blog>/", BlogView.as_view(), name="blog"),
    path("<str:blog>/<str:slug>/", BlogPostView.as_view(), name="blog_post"),
]
