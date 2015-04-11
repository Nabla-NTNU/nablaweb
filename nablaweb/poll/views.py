# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Poll, Choice, UserHasVoted


@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        choice = poll.choice_set.get(pk=request.POST['choice'])
        choice.vote(request.user)
    except (KeyError, Choice.DoesNotExist):
        messages.warning(request, 'Du valgte ikke et svaralternativ')
    except UserHasVoted:
        messages.error(request, 'Du har allerede stemt i denne avstemningen!')
    else:
        messages.success(request, u'Du har svart på "%s"' % poll.question)

    redirect_to = request.REQUEST.get('next', request.META.get('HTTP_REFERER', '/'))
    return redirect(redirect_to)
