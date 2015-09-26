import os

# This is useful for using custom python shells.

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nablaweb.settings.devel")
try:
    from django.conf import settings
except:
    print("Could not import Django modules.")
else:
    print("Imported Django modules.")
