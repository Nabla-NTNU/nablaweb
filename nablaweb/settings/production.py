# -*- coding: utf-8 -*-
from .base import *

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass


DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nabla_no',
        'USER': 'nabla_no',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'nabla_no',
    }
}

SESSION_COOKIE_DOMAIN = '.nabla.no'

BPC_TESTING = False
