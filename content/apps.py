"""
App config for content

This is still a real django app for legacy reasons.
It should perhaps be done away with.
"""
from django.apps import AppConfig


class ContentConfig(AppConfig):
    """
    Django app configuration for content
    """
    name = 'content'
    verbose_name = 'Innhold'
