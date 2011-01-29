# arrangement/views.py

from arrangement.models import Arrangement


# Administrasjon

def opprett(request, arr_id):
    pass

def status(request, arr_id):
    pass

def endre(request, arr_id):
    pass

def slett(request, arr_id):
    pass

def bekreft_sletting(request, arr_id):
    pass


# Offentlig

def oversikt(request):
    pass

def detaljer(request, arr_id):
    pass


# Bruker

def vis_bruker(request):
    pass

def meld_paa(request, arr_id):
    pass


# Eksporter

def vcal_arrangement(request, arr_id):
    pass

def vcal_bruker(request):
    pass
