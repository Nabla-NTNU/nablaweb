# -*- coding: utf-8 -*-
from .base import *
import os

DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(VARIABLE_CONTENT, os.environ.get('NABLAWEB_DB', 'sqlite.db')),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
}

# All epost blir sendt til terminalen, istedet for ut til brukerne.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Krevd av mediawiki_import
USE_TZ = True

# easy_thumbnail debugging
# Gjør at man får en feilmelding dersom thumbnail-taggen ikke klarer å lage ny
# thumbnail
THUMBNAIL_DEBUG = True
