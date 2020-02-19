"""
This module contains the AppConfig for the news app.
"""
from django.apps import AppConfig


class NewsConfig(AppConfig):
    """Configuration for news-app"""

    name = "nablapps.news"
    verbose_name = "Nyheter"

    def ready(self):
        # import from signals in order to register the callbacks
        from .signals import callback as _
