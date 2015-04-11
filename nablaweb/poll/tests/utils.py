import unittest
from datetime import datetime
from poll.models import Poll, Choice


def create_poll(question, *choices):
    poll = Poll.objects.create(question=question, publication_date=datetime(2020, 1, 1))
    for choice in choices:
        Choice.objects.create(poll=poll, choice=choice)
    return poll


class UserHasVotedMixin(unittest.TestCase):
    def assertUserHasVoted(self, user, poll):
        self.assertTrue(poll.user_has_voted(user))

    def assertUserHasNotVoted(self, user, poll):
        self.assertFalse(poll.user_has_voted(user))
