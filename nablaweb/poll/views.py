# -*- coding: utf-8 -*-

from poll.models import Poll, Choice
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    redirect_to = request.REQUEST.get('next', request.META.get('HTTP_REFERER', '/'))
    try:
        choice = poll.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        messages.add_message(request, messages.WARNING, 'Du valgte ikke et svaralternativ')
    else:
        vote_successful = choice.vote(request.user)

        if vote_successful:
            messages.add_message(request, messages.INFO, u'Du har svart på "%s"' % (poll.question))
        else:
            messages.add_message(request, messages.ERROR, 'Du har allerede stemt i denne avstemningen!')

    return redirect(redirect_to)
