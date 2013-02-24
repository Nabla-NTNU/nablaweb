# -*- coding: utf-8 -*-
# Django settings for nablaweb project.

# Mulige innstillinger for nablaweb
# Ting som (kanskje) må gjøres for å få det oppe og kjøre:
#  - Sette templatesmappe
#  - Database
#  - Media folder
#  - Media url

import os
from globalsettings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.dirname(__file__)

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
    ('Trygve','trygvebw@gmail.com'),
)

MANAGERS = ADMINS
# Må endres lokalt
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'develdb',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/var/www/nablaweb_devel/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://devel.nabla.no/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

MEDIA_DEV_MODE = DEBUG

DEV_MEDIA_URL = '/dev_static_generated/'

PRODUCTION_MEDIA_URL = 'http://gauss.nt.ntnu.no:346/_generated_media/'

GLOBAL_MEDIA_DIRS = (os.path.join(PROJECT_ROOT, '..', 'static'),)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'a()j2kxbwejl0y^jsk1*f#!=6na3pln6@fn!1ef6xra6(r3(%p'

ROOT_URLCONF = 'nablaweb.urls'

# Endres lokalt
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	("/home/trygvwii/nablaweb_devel/nablaweb/templates"),
)

LOGIN_URL = '/login/'

# Hvor passwd-fila til ntnulinuxserverne ligger på gauss. Må bli lastet ned
# regelmessig med cron eller noe lignende.
NTNU_PASSWD = '/home/hiasen/passwd'

STATIC_URL = "/static/"

STATICFILES_DIRS = (
    '/home/trygvwii/nablaweb_devel/static',
)
