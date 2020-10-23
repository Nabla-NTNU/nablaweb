"""
Django instillinger som er felles for alle instanser av nablaweb
Ikke bruk denne til å kjøre django med
Bruk heller devel.py eller production.py
"""
import os

from easy_thumbnails.conf import Settings as EasyThumbnailSettings

DEBUG = True

SITE_ID = 1
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "nabla.no"]

TIME_ZONE = "Europe/Oslo"
LANGUAGE_CODE = "nb"
USE_L10N = False  # don't use the locale of the server
DATE_FORMAT = "j. F Y"

DATE_INPUT_FORMATS = (
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%d/%m/%y",
    "%d.%m.%Y",
    "%d.%m.%y",
    "%d.%n.%Y",
    "%d.%n.%y",
)

TIME_INPUT_FORMATS = (
    "%H:%M:%S",
    "%H:%M",
    "%H",
)

# Gjør det enkelt å bruke relative paths
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
VARIABLE_CONTENT = os.environ.get("VARIABLE_CONTENT", os.path.join(PROJECT_ROOT, "var"))

# Absolute path to the directory that holds media.
MEDIA_ROOT = os.path.join(VARIABLE_CONTENT, "media")
PROTECTED_MEDIA_FOLDER = "protected_media"
PROTECTED_MEDIA_ROOT = os.path.join(VARIABLE_CONTENT, PROTECTED_MEDIA_FOLDER)
MEDIA_URL = "/media/"

STATIC_URL = "/static/"

# Mappe hvor alle statiske filer blir lagt etter at man kjører manage.py collectstatic
STATIC_ROOT = os.path.join(VARIABLE_CONTENT, "static_collected")

STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, "static"),)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django_node_assets.finders.NodeModulesFinder",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [os.path.join(PROJECT_ROOT, "templates")],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.static",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "sekizai.context_processors.sekizai",
                "nablapps.core.context_processors.get_primary_dir",
                "nablapps.core.context_processors.get_navbar_color",
            ],
        },
    }
]

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "nablaweb.urls"

INSTALLED_APPS = [
    ##########################
    # Internt utviklede apps #
    ##########################
    "nablapps.accounts",
    "nablapps.apply_committee",
    "nablapps.album",
    "nablapps.blog",
    "nablapps.com",
    "nablapps.contact",
    "nablapps.core",
    "nablapps.events",
    "nablapps.exchange",
    "nablapps.image",
    "nablapps.interactive",
    "nablapps.jobs",
    "nablapps.meeting_records",
    "nablapps.nabladet",
    "nablapps.nablaforum",
    "nablapps.nablashop",
    "nablapps.news",
    "nablapps.officeBeer",
    "nablapps.officeCalendar",
    "nablapps.podcast",
    "nablapps.poll",
    "nablapps.qrTickets",
    "nablaweb",
    ###########################
    # Eksternt utviklede apps #
    ###########################
    "bootstrap4",
    "django_comments",
    "django_node_assets",
    "easy_thumbnails",  # thumbnail-taggen i templates
    "image_cropping",  # gjør det mulig for staff å croppe opplastede bilder
    "filebrowser",
    "haystack",
    "hitcount",
    "markdown_deux",
    "sekizai",  # http://django-sekizai.readthedocs.org/en/latest/#
    "qr_code",
    "multi_email_field",
    "ckeditor",
    "ckeditor_uploader",
    "rest_framework",
    # Djangoting
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.flatpages",
    "django.contrib.humanize",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    # django-wiki
    "django_nyt",
    "mptt",
    "sorl.thumbnail",
    "wiki",
    "wiki.plugins.attachments",
    "wiki.plugins.notifications",
    "wiki.plugins.images",
    "wiki.plugins.macros",
    "wiki.plugins.links",
]


TEST_RUNNER = "django.test.runner.DiscoverRunner"

###########################
# App-spesifikke settings #
###########################


FILEBROWSER_DIRECTORY = ""

# ckeditor
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": [],
    },
    "basic": {
        "toolbar": "Basic",
        "toolbar_Basic": [
            {
                "name": "basicstyles",
                "items": [
                    "Bold",
                    "Italic",
                    "Underline",
                    "Smiley",
                    "SpecialChar",
                    "Mathjax",
                    "CodeSnippet",
                ],
            },
            {
                "name": "paragraph",
                "items": [
                    "NumberedList",
                    "BulletedList",
                    "JustifyLeft",
                    "JustifyCenter",
                    "JustifyRight",
                ],
            },
            {
                "name": "styles",
                "items": [
                    "Styles",
                    "Format",
                    "Font",
                    "FontSize",
                    "TextColor",
                    "BGColor",
                ],
            },
            {"name": "links", "items": ["Link", "Unlink", "Anchor"]},
        ],
        "mathJaxLib": "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS_SVG",
        "mathJaxClass": "mathjax-latex",
        "tabSpaces": 4,
        "extraPlugins": ",".join(
            [
                "mathjax",
                "codesnippet",
            ]
        ),
    },
}

# django.contrib.auth
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
AUTH_USER_MODEL = "accounts.NablaUser"

# easy-thumbnails/Django-image-cropping
THUMBNAIL_PROCESSORS = (
    "image_cropping.thumbnail_processors.crop_corners",
) + EasyThumbnailSettings.THUMBNAIL_PROCESSORS
THUMBNAIL_BASEDIR = "thumbnails"

# Haystack search
HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": os.path.join(VARIABLE_CONTENT, "whoosh_index"),
    },
}

# Sending email
DEFAULT_FROM_EMAIL = "noreply@nabla.no"

# Markdown deux
MARKDOWN_DEUX_STYLES = {
    "default": {"extras": {"code-friendly": None}, "safe_mode": "escape"},
    "unsafe": {
        "extras": {"code-friendly": None},
        # Allow raw HTML
        "safe_mode": False,
    },
}

# wiki
WIKI_REVISIONS_PER_HOUR = 500
WIKI_REVISIONS_PER_MINUTES = 20
WIKI_REVISIONS_PER_HOUR_ANONYMOUS = 0
WIKI_REVISIONS_PER_MINUTES_ANONYMOUS = 0
WIKI_ACCOUNT_HANDLING = False
WIKI_ACCOUNT_SIGNUP_ALLOWED = False

NODE_PACKAGE_JSON = os.path.join(PROJECT_ROOT, "package.json")
NODE_MODULES_ROOT = os.path.join(PROJECT_ROOT, "node_modules")
