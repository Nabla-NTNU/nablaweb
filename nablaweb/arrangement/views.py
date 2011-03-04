# arrangement/views.py

from nablaweb.arrangement.models import SimpleEvent, Event
from nablaweb.arrangement.forms import SimpleEventForm
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import Context, RequestContext, loader
import datetime

# Administrasjon

def create(request):
    if request.method == 'POST':
        form = SimpleEventForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            event = SimpleEvent(title=cd['title'],
                                summary=cd['summary'],
                                body=cd['body'],
                                location=cd['location'],
                                time=cd['time'],
                                )
            event.save()
    else:
        form = SimpleEventForm(
            initial={'time': datetime.datetime.now()},
            )
    return render_to_response('nablaweb/arrangement/templates/arrangement/opprett.html', RequestContext(request, {'form': form}))

def status(request, event_id):
    return HttpResponse("Not implemented.")

def edit(request, event_id):
    return HttpResponse("Not implemented.")

def delete(request, event_id):
    return HttpResponse("Not implemented.")


# Offentlig

def overview(request):
    return render_to_response('nablaweb/arrangement/templates/arrangement/overview.html', {'event_list': SimpleEvent.objects.all()})

def details(request, event_id):
    a = get_object_or_404(SimpleEvent, pk=event_id)
    return render_to_response('nablaweb/arrangement/templates/arrangement/details.html', {'event': a})


# Bruker

def show_user(request):
    return HttpResponse("Not implemented.")

def registration(request, event_id):
    return HttpResponse("Not implemented.")

def register(request, event_id):
    return HttpResponse("Not implemented.")


# Eksporter

def ical_event(request, event_id):
    a = get_object_or_404(Event, pk=event_id)
    t = loader.get_template('nablaweb/arrangement/templates/arrangement/icalendar.ics')
    c = Context({'event_list': (a,),})
    response = HttpResponse(t.render(c), mimetype='text/calendar')
    response['Content-Disposition'] = 'attachment; filename=Nabla_%s.ics' % a.title.replace(' ', '_')
    return response

def ical_user(request):
    return HttpResponse("Not implemented.")
