"""
Define configurations for the app blog
"""
from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Default blog config"""
    name = 'contentapps.blog'
    verbose_name = 'Blogg'
