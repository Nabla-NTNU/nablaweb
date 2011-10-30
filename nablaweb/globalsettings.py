# -*- coding: utf-8 -*-
# Django settings for nablaweb project.

# Mulige innstillinger for nablaweb
# Ting som (kanskje) må gjøres for å få det oppe og kjøre:
#  - Sette templatesmappe
#  - Database
#  - Media folder
#  - Media url

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Gjør det enkelt å bruke relative paths
PROJECT_ROOT = os.path.dirname(__file__)


ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS
# Må endres lokalt hvis du ikke bruker sqlite3
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_ROOT, '..', 'sqlite.db'), # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Oslo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'no-nb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.


# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# f.eks. http://nabla.no/static/
STATIC_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = ''

# django-mediagenerator setings (spør meg (andreros) om du lurer på noe)
##############################################################################
# mediagenerator kombinerer alle css og js-filer inn i en enkel fil. Dette
# gjør siden får mange færre HTTP requests. Den gjør også at vi kan bruke
# Compass/SASS til CSS-en, noe som er ytterst koselig.

# Debug: Serve files at DEV_MEDIA_URL
# False: Don't serve files (Do it yourself)
MEDIA_DEV_MODE = DEBUG

# Where mediagenerator serves files during debug
DEV_MEDIA_URL = '/dev_static_generated/'   # Serve files at localhost:8000/DEV_MEDIA_URL

# Where _generated_media_folder is available during production
PRODUCTION_MEDIA_URL = 'http://localhost/nablaweb/_generated_media/' 

# Full path to static folder
GLOBAL_MEDIA_DIRS = (os.path.join(PROJECT_ROOT, '..', 'static'),)

# Hent media bundles (ting som skal kombineres/kompileres/komprimeres)
from media_bundles import *
##############################################################################

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'a()j2kxbwejl0y^jsk1*f#!=6na3pln6@fn!1ef6xra6(r3(%p'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'mediagenerator.middleware.MediaMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
)

ROOT_URLCONF = 'nablaweb.urls'

# Endres lokalt
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    # Våre ting
    'news',
    'accounts',
    'avatar',
    'events',
    'content',
    'jobs',
    'gallery',
    'bedpres',
    'homepage',
    'com',
    'quotes',
    'feedback',
    'nabladet',
    # Eksterne ting
    'math_captcha', # sudo pip install django-match-captcha
    'mediagenerator', # sudo pip install django-mediagenerator
    # Djangoting
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.markup',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.humanize',
)

AUTH_PROFILE_MODULE= 'accounts.UserProfile'
LOGIN_URL = '/login/'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'events.context_processors.upcoming_events', # Legger til upcoming_events i alle templates.
    'jobs.views.activej',
    'quotes.context_processors.random_quote',
    'events.context_processors.current_month_calendar',
   )


# Hvor passwd-fila til ntnulinuxserverne ligger på gauss. Må bli lastet ned
# regelmessig med cron eller noe lignende.
NTNU_PASSWD = '/home/hiasen/passwd'

# MATH CAPTCHA
MATH_CAPTCHA_QUESTION = ''
MATH_CAPTCHA_NUMBERS = range(0,40)
MATH_CAPTCHA_OPERATORS = '+-*/%'
