# -*- coding: utf-8 -*-

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'nablapps.accounts'
    verbose_name = 'Brukerkontoer'

    def ready(self):
        super(AccountsConfig, self).ready()
        from .signals import register_signals
        register_signals()
