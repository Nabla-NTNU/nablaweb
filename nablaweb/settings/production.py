# -*- coding: utf-8 -*-
import os
import pymysql
from .base import *

pymysql.install_as_MySQLdb()
get_env = os.environ.get

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_env('MYSQL_DATABASE'),
        'USER': get_env('MYSQL_USER'),
        'PASSWORD': get_env('MYSQL_USER_PASSWORD'),
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
