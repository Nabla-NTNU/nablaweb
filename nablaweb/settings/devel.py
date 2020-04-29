# -*- coding: utf-8 -*-
import os

from .base import *

DEBUG = True

SECRET_KEY = "my_not_so_secret_development_key"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(
            VARIABLE_CONTENT, os.environ.get("NABLAWEB_DB", "sqlite.db")
        ),  # noqa: F405
    }
}

CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}

# All epost blir sendt til terminalen, istedet for ut til brukerne.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# easy_thumbnail debugging
# Gjør at man får en feilmelding dersom thumbnail-taggen ikke klarer å lage ny
# thumbnail
THUMBNAIL_DEBUG = True
