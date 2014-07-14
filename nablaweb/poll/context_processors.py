# -*- coding: utf-8 -*-

from poll.models import Poll

def poll_context(request):
    context = {}
    try:
        poll = Poll.objects.filter(is_current=True)[0]
        context['poll'] = poll
        context['poll_has_voted'] = poll.user_has_voted(request.user)
        context['poll_total_votes'] = poll.get_total_votes()
    except:
        pass
    return context
