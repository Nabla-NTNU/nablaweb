# -*- coding: utf-8 -*-
import os
import pymysql
from .base import *

pymysql.install_as_MySQLdb()
get_env = os.environ.get

DEBUG = bool(get_env('DEBUG', False))
ADMINS = [("Django-logging", "django-log@abel.nabla.no")]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_env('MYSQL_DATABASE'),
        'USER': get_env('MYSQL_USER'),
        'PASSWORD': get_env('MYSQL_USER_PASSWORD'),
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': get_env('DJANGO_LOG_PATH', '/var/log/django/nablaweb/error.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

SESSION_COOKIE_DOMAIN = '.nabla.no'

BPC_TESTING = False
