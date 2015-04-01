# -*- coding: utf-8 -*-
"""
Tests for poll app
"""

from django.test import TestCase
from datetime import datetime
from django.contrib.auth import get_user_model
User = get_user_model()

from poll.models import Poll, Choice, UserHasVoted


class TestPoll(TestCase):

    def setUp(self):
        self.create_a_poll()
        self.create_some_users()
        self.first_user = self.users[0]
        self.some_choice = self.poll.choice_set.first()

    def create_some_users(self):
        self.users = [User.objects.create(username=u"username%d" % i) for i in range(10)]

    def create_a_poll(self):
        self.poll = Poll.objects.create(
            question=u"Hva er et spørsmål?",
            publication_date=datetime(2020, 1, 1))
        Choice.objects.create(
            poll=self.poll,
            choice=u"Å svare eller ikke svare, det er spørsmålet.")
        Choice.objects.create(
            poll=self.poll,
            choice=u"Spørsmålet er svaret")

    def test_a_user_votes_once(self):
        self.some_choice.vote(self.first_user)

        self.assertTrue(self.poll.user_has_voted(self.first_user))
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
        choices = self.poll.choice_set.all()
        for user in self.users[:5]:
            choices[0].vote(user)

        for user in self.users[5:]:
            choices[1].vote(user)

        num_users = len(self.users)
        self.assertEqual(num_users, self.poll.get_total_votes())


class CurrentPollTest(TestCase):

    def setUp(self):
        self.first_poll = Poll.objects.create(
            question=u"Hvem er du?",
            publication_date=datetime(2020, 1, 1))

        self.second_poll = Poll.objects.create(
            question=u"Hvor kommer verden fra?",
            publication_date=datetime(2020, 1, 1))

    def assert_is_current_poll(self, poll):
        self.assertEqual(poll, Poll.objects.current_poll())

    def test_last_created_poll_is_current(self):
        self.assert_is_current_poll(self.second_poll)

    def test_set_is_current(self):
        self.first_poll.is_current = True
        self.first_poll.save()

        # Get second_poll again because it has been updated
        second_poll = Poll.objects.get(pk=self.second_poll.pk)

        self.assert_is_current_poll(self.first_poll)
        self.assertFalse(second_poll.is_current)
