"""
App configs for poll app
"""
from django.apps import AppConfig


class PollConfig(AppConfig):
    """Default poll config"""
    name = 'nablapps.poll'
    verbose_name = 'Avstemninger'
