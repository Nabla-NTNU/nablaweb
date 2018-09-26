"""
Context processors for poll app
"""
from .models import Poll


def poll_context(request):
    """
    Return a context containing:

    'poll': <The current poll>
    'poll_has_voted': <Bool indicating whether the logged in user has voted on the current poll>
    'poll_total_votes': <Total number of votes cast in the current poll>

    or an empty context if there is no current poll.
    """

    try:
        poll = Poll.objects.current_poll()
        return {
            'poll': poll,
            'poll_has_voted': poll.user_has_voted(request.user),
            'poll_total_votes': poll.get_total_votes()
        }
    except Poll.DoesNotExist:
        return {}
