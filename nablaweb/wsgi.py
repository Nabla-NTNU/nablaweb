"""
WSGI config for nablaweb.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nablaweb.settings.devel")
application = get_wsgi_application()
