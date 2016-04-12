"""
Settings used for testing the likes-app without all the installed apps
for the entire project.
This is because it takes a lot of time to run all the migrations for all the apps in the nablaweb project.
"""
import os

DEBUG = True
BASE_DIR = os.path.dirname(__file__)
SECRET_KEY = 'very_secret'
ROOT_URLCONF = "likes.tests.urls"
STATIC_URL = '/static/'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'likes',
    'likes.tests.dummyapp',
    'sekizai',
]
MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'sqlite.db'),
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'sekizai.context_processors.sekizai',
            ],
        },
    }
]

LOGIN_URL = '/login/'
