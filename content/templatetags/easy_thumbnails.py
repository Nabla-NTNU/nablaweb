"""
A hack to be able to load easy_thumbnails templatetags using
{% load easy_thumbnails %}
instead of
{% lead thumbnail %}.

The reason for doing this is that sorl.thumbnail and easy_thumbnails both
name their templatetag module 'thumbnail' and one gets conflicts.
The reason for using both thumbnail libraries is that they are used in different apps on pypi.
"""
from easy_thumbnails.templatetags.thumbnail import *
