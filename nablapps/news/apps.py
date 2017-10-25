from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = 'nablapps.news'
    verbose_name = 'Nyheter'

    def ready(self):
        from .signals import callback
