# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth import get_user_model
from poll.models import UserHasVoted
from .utils import UserHasVotedMixin, create_poll

User = get_user_model()


class TestPoll(UserHasVotedMixin, TestCase):

    def setUp(self):
        self.poll = create_poll(
            u"Hva er et spørsmål?",
            u"Å svare eller ikke svare, det er spørsmålet.",
            u"Spørsmålet er svaret."
        )
        self.users = [User.objects.create(username=u"username%d" % i) for i in range(10)]
        self.first_user = self.users[0]
        self.some_choice = self.poll.choices.first()

    def test_a_user_votes_once(self):
        self.some_choice.vote(self.first_user)

        self.assertUserHasVoted(self.first_user, self.poll)
        self.assertEqual(1, self.some_choice.votes)

    def test_a_user_tries_to_vote_twice(self):
        self.some_choice.vote(self.first_user)

        with self.assertRaises(UserHasVoted):
            self.some_choice.vote(self.first_user)

    def test_multiple_users_vote_for_the_same_thing(self):
        for user in self.users:
            self.some_choice.vote(user)

        num_users = len(self.users)
        self.assertEqual(num_users, self.some_choice.votes)
        self.assertEqual(num_users, self.poll.users_voted.count())

    def test_users_voting_for_different_things(self):
        first_choice, second_choice = self.poll.choices.all()[:2]
        for user in self.users[:5]:
            first_choice.vote(user)

        for user in self.users[5:]:
            second_choice.vote(user)

        num_users = len(self.users)
        self.assertEqual(num_users, self.poll.get_total_votes())
