# Views for modulen wikidj

from django.http import HttpResponse
import wiki_utils
import WikiSettings

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

def user_logged_in(request):
    return HttpResponse(user)

def user_specific_pages(request):
    # Innstillinger, overvaakningsliste, etc., men ikke logg ut.
    return HttpResponse(user_pages)

def user_logout(request):
    # Boer integreres med Nabla-siden ellers
    return HttpResponse(logout)

def search(request):
    return HttpResponse(search_field)
