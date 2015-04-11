# -*- coding: utf-8 -*-

from .models import Poll


def poll_context(request):
    try:
        poll = Poll.objects.current_poll()
        return {
            'poll': poll,
            'poll_has_voted': poll.user_has_voted(request.user),
            'poll_total_votes': poll.get_total_votes()
        }
    except Poll.DoesNotExist:
        return {}
