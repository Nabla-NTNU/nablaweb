"""
WSGI config for nablaweb.
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nablaweb.settings.devel")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
