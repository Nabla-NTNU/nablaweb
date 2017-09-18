default_app_config = 'nablapps.bedpres.apps.BedpresConfig'

from django.conf import settings
from bpc_client.client import DefaultClientFactory


DefaultClientFactory.configure(
    {"BPC_FORENING": settings.BPC_FORENING,
     "BPC_KEY": settings.BPC_KEY,
     "BPC_TESTING": settings.BPC_TESTING}
)

