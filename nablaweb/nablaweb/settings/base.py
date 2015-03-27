# -*- coding: utf-8 -*-
# Django instillinger som er felles for alle instanser av nablaweb
# Ikke bruk denne til å kjøre django med
# Bruk heller devel.py eller production.py

# Django settings
#########################################

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "nabla.no"]

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'a()j2kxbwejl0y^jsk1*f#!=6na3pln6@fn!1ef6xra6(r3(%p'

TIME_ZONE = 'Europe/Oslo'
LANGUAGE_CODE = 'nb'
USE_L10N = True  # use locale dates, numbers etc.
DATE_FORMAT = 'j. F Y'

# Gjør det enkelt å bruke relative paths
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
VARIABLE_CONTENT = os.path.join(PROJECT_ROOT, '..', 'var')

# Absolute path to the directory that holds media.
MEDIA_ROOT = os.path.join(VARIABLE_CONTENT, 'media')
MEDIA_URL = '/media/'

STATIC_URL = '/static/'

# Mappe hvor alle statiske filer blir lagt etter at man kjører
# manage.py collectstatic
STATIC_ROOT = os.path.join(VARIABLE_CONTENT, 'static_collected')

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, '..', 'static'),
)

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
    'accounts',  # Inneholder UserProfile med ekstra informasjon.
    'events',   # Arrangement. Arver nyheter.
    'jobs',     # Stillingsannonser og firmaer
    'bedpres',  # Utvider events med BPC-tilkobling. Arver events.
    'com',      # Viser sider for komiteene.
    'nabladet',  # Liste over nablad. Arver news.
    'meeting_records',  # Møtereferater fra styremøter og SKE
    'poll',     # Spørreundersøkelser
    'search',
    'podcast',

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

    # Haystack er en app for søking. (Krever 2.0.0 beta samt Whoosh!)
    'haystack',

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
]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',

    'sekizai.context_processors.sekizai',

    'events.context_processors.upcoming_events',     
    'jobs.views.active_jobs',
    'com.context_processors.com_context',
    'poll.context_processors.poll_context',
    'nablaweb.context_processors.primary_dir',
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
from easy_thumbnails.conf import Settings as easy_thumb_Settings
easy_thumb_settings = easy_thumb_Settings
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + easy_thumb_settings.THUMBNAIL_PROCESSORS
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
