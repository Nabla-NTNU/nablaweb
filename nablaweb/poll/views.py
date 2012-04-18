# -*- coding: utf-8 -*-

from poll.models import Poll, Choice
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        choice = poll.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return HttpResponse("Du valgte ikke et svaralternativ.")
    else:
        if (choice.votes):
            choice.votes += 1
        else:
            choice.votes = 1
        choice.save()
        return HttpResponseRedirect(reverse('news_list')) # redirect hvor?
