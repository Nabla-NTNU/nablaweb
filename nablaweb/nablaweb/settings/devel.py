# -*- coding: utf-8 -*-
from .base import *
import os


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(VARIABLE_CONTENT, os.environ.get('NABLAWEB_DB', 'sqlite.db')),
    }
}

# All epost blir sendt til terminalen, istedet for ut til brukerne.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Debug toolbar
###################################################
DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}
# IP-er som har tilgang til debug toolbar. Bruk funksjonen under for å legge til din
INTERNAL_IPS = ['127.0.0.1', ]

# Informasjon som debug toolbar viser
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
    # Trenger installasjon, se linken:
    # https://github.com/jbalogh/django-debug-cache-panel
    'cache_panel.panel.CacheDebugPanel' 
)
# Funksjon for å starte debug toolbar
# Tar inn IP-adresser som skal ha tilgang til å vise debug toolbar
def use_debug_toolbar(*ip_addresses):
    for ip in ip_addresses:
        INTERNAL_IPS.append(ip)
    INSTALLED_APPS.append('debug_toolbar')
    INSTALLED_APPS.append('cache_panel')
    MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')

# bedpres
##################################################
BPC_URL = 'http://testing.bedriftspresentasjon.no/remote/' #Testserver
