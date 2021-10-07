# -*- coding: utf-8 -*-
import os

import pymysql

# Import all common settings
from .base import *  # noqa: F401, F403

pymysql.version_info = (
    1,
    4,
    2,
    "final",
    0,
)  # PyMySQL needs to lie about its version for django>=2.2
pymysql.install_as_MySQLdb()
get_env = os.environ.get

DEBUG = bool(get_env("DEBUG", False))
ADMINS = [("Django-logging", "django-log@abel.nabla.no")]
TEMPLATE_DEBUG = False

SECRET_KEY = get_env("SECRET_KEY")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": get_env("MYSQL_DATABASE"),
        "USER": get_env("MYSQL_USER"),
        "PASSWORD": get_env("MYSQL_USER_PASSWORD"),
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"timestamp": {"format": "%(asctime)s %(message)s"}},
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": get_env(
                "DJANGO_LOG_PATH", "/var/log/django/nablaweb/error.log"
            ),
            "formatter": "timestamp",
        },
    },
    "loggers": {"django": {"handlers": ["file"], "level": "ERROR", "propagate": True}},
}


FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
