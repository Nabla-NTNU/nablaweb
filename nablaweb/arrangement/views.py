# arrangement/views.py

from arrangement.models import Arrangement
from django.shortcuts import render_to_response, get_object_or_404

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
    return render_to_response('nablaweb/arrangement/templates/arrangement/oversikt.html', {'arrangementliste': Arrangement.objects.all()})

def detaljer(request, arr_id):
    a = get_object_or_404(Arrangement, pk=arr_id)
    return render_to_response('nablaweb/arrangement/templates/arrangement/detaljer.html', {'arrangement': a})


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
