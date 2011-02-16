# arrangement/views.py

from arrangement.models import Event
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import Context, loader


# Administrasjon

def create(request, arr_id):
    pass

def status(request, arr_id):
    pass

def edit(request, arr_id):
    pass

def delete(request, arr_id):
    pass

def confirm_deletion(request, arr_id):
    pass


# Offentlig

def overview(request):
    return render_to_response('nablaweb/arrangement/templates/arrangement/overview.html', {'event_list': Event.objects.all()})

def details(request, arr_id):
    a = get_object_or_404(Event, pk=event_id)
    return render_to_response('nablaweb/arrangement/templates/arrangement/details.html', {'event': a})


# Bruker

def show_user(request):
    pass

def registration(request, event_id):
    pass

def register(request, event_id):
    pass


# Eksporter

def ical_event(request, arr_id):
    a = get_object_or_404(Event, pk=arr_id)
    t = loader.get_template('nablaweb/arrangement/templates/arrangement/icalendar.ics')
    c = Context({'event_list': (a,),})
    response = HttpResponse(t.render(c), mimetype='text/calendar')
    response['Content-Disposition'] = 'attachment; filename=Nabla_%s.ics' % a.title.replace(' ', '_')
    return response

def ical_user(request):
    pass
