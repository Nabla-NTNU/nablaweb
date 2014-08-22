# -*- coding: utf-8 -*-
# Django instillinger som er felles for alle instanser av nablaweb
# Ikke bruk denne til å kjøre django med
# Bruk heller devel.py eller production.py

# Django settings
#########################################

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Gjør det enkelt å bruke relative paths
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
VARIABLE_CONTENT = os.path.join(PROJECT_ROOT, '..', 'var')

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "nabla.no"]


ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # 'mysql' eller 'sqlite3'
        'NAME': os.path.join(VARIABLE_CONTENT, 'sqlite.db'), # Or path to database file if using sqlite3.
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

TIME_ZONE = 'Europe/Oslo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'nb'

DATE_FORMAT = 'j. F Y'

SITE_ID = 1

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Additional paths to search for fixtures
FIXTURE_DIRS = (os.path.join(PROJECT_ROOT, 'nablaweb', 'fixtures'),)

# Absolute path to the directory that holds media.
MEDIA_ROOT = os.path.join(VARIABLE_CONTENT, 'media')
MEDIA_URL = '/media/'

# f.eks. http://nabla.no/static/
STATIC_URL = '/static/'

# Mappe hvor alle statiske filer blir lagt etter at man kjører
# manage.py collectstatic
STATIC_ROOT = os.path.join(VARIABLE_CONTENT, 'static_collected')

STATICFILES_DIRS = (
        os.path.join(PROJECT_ROOT, '..', 'static'),
)

ADMIN_MEDIA_PREFIX = '/static/admin/'

##############################################################################

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'a()j2kxbwejl0y^jsk1*f#!=6na3pln6@fn!1ef6xra6(r3(%p'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'sessionprofile.middleware.SessionProfileMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
]

ROOT_URLCONF = 'nablaweb.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = [
    ##########################
    # Internt utviklede apps #
    ##########################
    'content',  # Abstrakt: created, updated, created by, updated by. 
    'news',     # Nyheter. Arver content.
    'accounts', # Inneholder UserProfile med ekstra informasjon.
    'events',   # Arrangement. Arver nyheter.
    'jobs',     # Stillingsannonser og firmaer
    'bedpres',  # Utvider events med BPC-tilkobling. Arver events.
    'com',      # Viser sider for komiteene.
    'nabladet', # Liste over nablad. Arver news.
    'meeting_records', # Møtereferater fra styremøter og SKE
    'poll',     # Spørreundersøkelser
    'skraattcast',
    'search',

    ###########################
    # Eksternt utviklede apps #
    ###########################

    # Sessionprofile gjør det mulig å logge direkte inn på blant annet Wikien,
    # phpBB, og annet, hvis man er logget på Nablaweb
    'sessionprofile',

    # Django-image-cropping (pip install) gjør det mulig for staff å croppe
    # opplastede bilder
    'easy_thumbnails', # thumbnail-taggen i templates
    'image_cropping', # Admindelen

    # South migrations 
    # Når det gjøres endringer i modeller må etterfulges av kommandoen
    # ./manage.py migrate --auto
    'south',

    # http://django-sekizai.readthedocs.org/en/latest/#
    'sekizai',

    'bootstrap3',
    'markdown_deux',

    # Djangoting
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    # Flatpages gjør at vi enkelt kan legge til sider som kun inneholder tekst,
    # på hvilken url "vi" vil. Teksten lagres i databasen.
    'django.contrib.flatpages',
    # Humanize legger til nyttige template-tags, som konverterer maskintid til
    # menneskelig leselig tid, f.eks. "i går".
    'django.contrib.humanize',
    'django.contrib.staticfiles',

    # Haystack. Krever 2.0.0 beta samt Whoosh!
    'haystack',
]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',

    'sekizai.context_processors.sekizai',

    'events.context_processors.upcoming_events',     
    'jobs.views.activej',
    'com.context_processors.com_context',
    'poll.context_processors.poll_context',
    'nablaweb.context_processors.primary_dir',
)

###########################
# App-spesifikke settings #
###########################


# Contrib.auth
##################################################
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
AUTH_USER_MODEL = 'accounts.NablaUser'


# easy-thumbnails/Django-image-cropping
###################################################
from easy_thumbnails.conf import Settings as easy_thumb_Settings
easy_thumb_settings = easy_thumb_Settings
THUMBNAIL_PROCESSORS = (
        'image_cropping.thumbnail_processors.crop_corners',
) + easy_thumb_settings.THUMBNAIL_PROCESSORS
THUMBNAIL_BASEDIR = 'thumbnails'

# Haystack search
##################################################
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(VARIABLE_CONTENT, 'whoosh_index'),
    },
}

# Sending email
##################################################
DEFAULT_FROM_EMAIL='noreply@nabla.no'


# South
#############################################
SOUTH_MIGRATION_MODULES = {
        'easy_thumbnails': 'easy_thumbnails.south_migrations',
    }
