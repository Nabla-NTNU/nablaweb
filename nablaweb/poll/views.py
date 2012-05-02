# -*- coding: utf-8 -*-

from poll.models import Poll, Choice
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    redirect_to = request.REQUEST.get('next', request.META.get('HTTP_REFERER', '/'))
    try:
        choice = poll.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        messages.add_message(request, messages.WARNING, 'Du valgte ikke et svaralternativ')
        return redirect(redirect_to)
    else:
        if (request.user in poll.users_voted.all()):
            messages.add_message(request, messages.ERROR, 'Du har allerede stemt i denne avstemningen!')
            return redirect(redirect_to)
        else:
            if (choice.votes):
                choice.votes += 1
            else:
                choice.votes = 1
            choice.save()
            poll.users_voted.add(request.user)
            messages.add_message(request, messages.INFO, u'Du har svart på "%s"' % (poll.question))
            return redirect(redirect_to)
