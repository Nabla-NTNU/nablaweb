# Views for modulen wikidj

from django.http import HttpResponse

def header(request):
    return HttpResponse(pagetitle)
    
def pagecontent_formatted(request):
    return HttpResponse(content_formatted)
    
def pagehistory_formatted(request):
    return HttpResponse(history_formatted)
    
def pageactions_formatted(request):
    # Slett, flytt, etc.
    # Selve sidene haandteres av pagecontent_formatted.
    return HttpResponse(actions_formatted)
