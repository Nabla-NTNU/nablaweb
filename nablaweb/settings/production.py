# -*- coding: utf-8 -*-
import os
import pymysql
from .base import *

pymysql.install_as_MySQLdb()
get_env = os.environ.get

DEBUG = bool(get_env('DEBUG', False))
ADMINS = [("Django-logging", "django-log@abel.nabla.no")]
TEMPLATE_DEBUG=False

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
    'formatters': {
        'timestamp': {
            'format': '%(asctime)s %(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': get_env('DJANGO_LOG_PATH', '/var/log/django/nablaweb/error.log'),
            'formatter': 'timestamp',
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

BPC_TESTING = False

FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
