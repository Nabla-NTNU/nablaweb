# -*- coding: utf-8 -*-
# Django settings for nablaweb project.

# Mulige innstillinger for nablaweb
# Ting som (kanskje) må gjøres for å få det oppe og kjøre:
#  - Sette templatesmappe
#  - Database
#  - Media folder
#  - Media url


# Django settings
#########################################

import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Gjør det enkelt å bruke relative paths
PROJECT_ROOT = os.path.dirname(__file__)

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "nabla.no"]


ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS
# Må endres lokalt hvis du ikke bruker sqlite3
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # 'mysql' eller 'sqlite3'
        'NAME': os.path.join(PROJECT_ROOT, '..', 'sqlite.db'), # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        #'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        #'LOCATION': '127.0.0.1:11211'
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
LANGUAGE_CODE = 'nb'

DATE_FORMAT = 'j. F Y'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.


# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Additional paths to search for fixtures
FIXTURE_DIRS = (os.path.join(PROJECT_ROOT, 'nablaweb', 'fixtures'),)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, '..', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# f.eks. http://nabla.no/static/
STATIC_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# True: Serve files at DEV_MEDIA_URL
# False: Don't serve files (Do it yourself)
# Noen som vet om denne variabelen brukes noe sted?
MEDIA_DEV_MODE = DEBUG

# Full path to static folder
# Variabelen heter media fordi mediagenerator ikke er helt up to date
# Mediagenerator er ikke lenger i bruk, men variabelen brukes i urls.py
GLOBAL_MEDIA_DIRS = (os.path.join(PROJECT_ROOT, '..', 'static'),)

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
    # Fjernet: Ikke i bruk
    # 'mediagenerator.middleware.MediaMiddleware',
    'django.middleware.common.CommonMiddleware',
    'sessionprofile.middleware.SessionProfileMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'pybb.middleware.PybbMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Bruk use_debug_toolbar(din_ip) for å skru på denne
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
]

ROOT_URLCONF = 'nablaweb.urls'

# Endres lokalt
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
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
    # 'feedback', # Hva gjør egentlig denne? Virker ikke som den trengs for at
                  # tilbakemeldings-formen skal fungere.
    # 'homepage', # Viser news og events sammen. Ikke i bruk.

    ###########################
    # Eksternt utviklede apps #
    ###########################

    # Debug toolbar viser informasjon om sidelastingen For å skru den på, bruk
    # funksjonen use_debug_toolbar(din_ip) i settings.py
    #'debug_toolbar',

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

    # Djangoting
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.markup',
    'django.contrib.messages',
    'django.contrib.admin',
    # Flatpages gjør at vi enkelt kan legge til sider som kun inneholder tekst,
    # på hvilken url "vi" vil. Teksten lagres i databasen.
    'django.contrib.flatpages',
    # Humanize legger til nyttige template-tags, som konverterer maskintid til
    # menneskelig leselig tid, f.eks. "i går".
    'django.contrib.humanize',
    
    # Alt som er nodvendig for pybbm
    #'pybb',
    #'pytils',
    #'pure_pagination',
    
    # Haystack. Krever 2.0.0 beta samt Whoosh!
    'haystack',
]



TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',

    'events.context_processors.upcoming_events',     
    'jobs.views.activej',
    #'pybb.context_processors.processor',
    'com.context_processors.com_context',
    'poll.context_processors.poll_context',
    'context_processors.primary_dir',
    'context_processors.xkcd',
)

###########################
# App-spesifikke settings #
###########################

# bedpres
##################################################
#BPC_URL = 'https://www.bedriftspresentasjon.no/remote/'
BPC_URL = 'http://testing.bedriftspresentasjon.no/remote/' #Testserver

# Contrib.auth
##################################################
AUTH_PROFILE_MODULE= 'accounts.UserProfile'
LOGIN_URL = '/login/'


# Math captcha
##################################################
MATH_CAPTCHA_QUESTION = ''
MATH_CAPTCHA_NUMBERS = range(0,40)
MATH_CAPTCHA_OPERATORS = '+-*/%'


# Debug toolbar
###################################################
DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}
# IP-er som har tilgang til debug toolbar. Bruk funksjonen under for å legge til din
INTERNAL_IPS = ['127.0.0.1', ]

# Informasjon som debug toolbar viser
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
    # Trenger installasjon, se linken:
    # https://github.com/jbalogh/django-debug-cache-panel
    'cache_panel.panel.CacheDebugPanel' 
)
# Funksjon for å starte debug toolbar
# Tar inn IP-adresser som skal ha tilgang til å vise debug toolbar
def use_debug_toolbar(*ip_addresses):
    for ip in ip_addresses:
        INTERNAL_IPS.append(ip)
    INSTALLED_APPS.append('debug_toolbar')
    INSTALLED_APPS.append('cache_panel')
    MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')


# Django-image-cropping
###################################################
from easy_thumbnails.conf import Settings as easy_thumb_Settings
easy_thumb_settings = easy_thumb_Settings
THUMBNAIL_PROCESSORS = (
        'image_cropping.thumbnail_processors.crop_corners',
) + easy_thumb_settings.THUMBNAIL_PROCESSORS


# PyBBm
##################################################
PYBB_DEFAULT_TITLE = 'Forum'
PYBB_DEFAULT_AUTOSUBSCRIBE = False
PYBB_FREEZE_FIRST_POST = False
PYBB_SIGNATURE_MAX_LINES = 0
PYBB_SIGNATURE_MAX_LENGTH = 0
PYBB_DEFAULT_TIME_ZONE = 1
PYBB_MARKUP = 'markdown'
PYBB_ENABLE_SELF_CSS = True


# Haystack search
##################################################
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

try:
    from local_settings import *
except ImportError:
    pass


# Sending email
##################################################
DEFAULT_FROM_EMAIL='noreply@nabla.no'



