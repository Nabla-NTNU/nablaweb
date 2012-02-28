# -*- coding: utf-8 -*-

from poll.models import Poll, Choice
from django.shortcut import get_object_or_404
from django.http import RequestContext, HttpResponse, HttpResponseRedirect

def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        choice = poll.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return HttpResponse("Du valgte ikke et svaralternativ.")
    else:
        choice.votes += 1
        choice.save()
        return HttpResponseRedirect(reverse('')) # redirect hvor?
