from django.http import HttpResponse

def index(request):
    return HttpResponse("Dette er en test.")

