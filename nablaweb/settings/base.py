# -*- coding: utf-8 -*-
# Django instillinger som er felles for alle instanser av nablaweb
# Ikke bruk denne til å kjøre django med
# Bruk heller devel.py eller production.py

# Django settings
#########################################

import os
from easy_thumbnails.conf import Settings as EasyThumbnailSettings

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "nabla.no"]

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'a()j2kxbwejl0y^jsk1*f#!=6na3pln6@fn!1ef6xra6(r3(%p'

TIME_ZONE = 'Europe/Oslo'
LANGUAGE_CODE = 'nb'
USE_L10N = False  # don't use the locale of the server
DATE_FORMAT = 'j. F Y'

DATE_INPUT_FORMATS = (
    '%Y-%m-%d',
    '%d/%m/%Y',
    '%d/%m/%y',
    '%d.%m.%Y',
    '%d.%m.%y',
    '%d.%n.%Y',
    '%d.%n.%y',)

TIME_INPUT_FORMATS = (
    '%H:%M:%S',
    '%H:%M',
    '%H',)

# Gjør det enkelt å bruke relative paths
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
VARIABLE_CONTENT = os.path.join(PROJECT_ROOT, 'var')

# Absolute path to the directory that holds media.
MEDIA_ROOT = os.path.join(VARIABLE_CONTENT, 'media')
MEDIA_URL = '/media/'

STATIC_URL = '/static/'

FILEBROWSER_DIRECTORY = ''

# Mappe hvor alle statiske filer blir lagt etter at man kjører
# manage.py collectstatic
STATIC_ROOT = os.path.join(VARIABLE_CONTENT, 'static_collected')

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    'djangobower.finders.BowerFinder'
)

BOWER_COMPONENTS_ROOT = os.path.join(PROJECT_ROOT)

ADMIN_MEDIA_PREFIX = '/static/admin/'

##############################################################################

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'sessionprofile.middleware.SessionProfileMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # django-wiki
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
    'accounts',  # Inneholder UserProfile med ekstra informasjon.
    'jobs',     # Stillingsannonser og firmaer
    'bedpres',  # Utvider events med BPC-tilkobling. Arver events.
    'com',      # Viser sider for komiteene.
    'nabladet',  # Liste over nablad. Arver news.
    'meeting_records',  # Møtereferater fra styremøter og SKE
    'poll',     # Spørreundersøkelser
    'podcast',
    'interactive',

    ###########################
    # Eksternt utviklede apps #
    ###########################

    # Sessionprofile gjør det mulig å logge direkte inn på blant annet Wikien,
    # phpBB, og annet, hvis man er logget på Nablaweb
    'sessionprofile',

    # Django-image-cropping (pip install) gjør det mulig for staff å croppe
    # opplastede bilder
    'easy_thumbnails',  # thumbnail-taggen i templates
    'image_cropping',  # Admindelen

    # http://django-sekizai.readthedocs.org/en/latest/#
    'sekizai',

    'bootstrap3',
    'markdown_deux',
    'django_comments',

    # Bower handterer frontend pakker
    'djangobower',

    # Haystack er en app for søking. (Krever 2.0.0 beta samt Whoosh!)
    'haystack',

    # Filebrowser
    'grappelli',
    'filebrowser',

    # Djangoting
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',

    # django-wiki
    'django_nyt',
    'mptt',
    'sorl.thumbnail',
    'wiki',
    'wiki.plugins.attachments',
    'wiki.plugins.notifications',
    'wiki.plugins.images',
    'wiki.plugins.macros',
]

BOWER_INSTALLED_APPS = (
    'jquery#1.9.x',
    'bootstrap',
    'rangy',
    'font-awesome',
    'pixi.js',
    'PhysicsJS',
    'requirejs',
    'jquery-file-upload'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',

    'sekizai.context_processors.sekizai',

    'nablaweb.context_processors.get_primary_dir',
    'nablaweb.context_processors.get_primary_dir',
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

###########################
# App-spesifikke settings #
###########################

# django.contrib.auth
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
AUTH_USER_MODEL = 'accounts.NablaUser'

# easy-thumbnails/Django-image-cropping
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + EasyThumbnailSettings.THUMBNAIL_PROCESSORS
THUMBNAIL_BASEDIR = 'thumbnails'

# Haystack search
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(VARIABLE_CONTENT, 'whoosh_index'),
    },
}

# Sending email
DEFAULT_FROM_EMAIL = 'noreply@nabla.no'

# Markdown deux
MARKDOWN_DEUX_STYLES = {
    "default": {
        "extras": {
            "code-friendly": None,
        },
        "safe_mode": "escape",
    },
    "unsafe": {
        "extras": {
            "code-friendly": None,
        },
        # Allow raw HTML
        "safe_mode": False,
    }
}

# BPC - api keys
BPC_FORENING = '3'
BPC_KEY = 'a88fb706bc435dba835b89ddb2ba4debacc3afe4'
BPC_TESTING = True
