""" Tests for the
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from nablapps.poll.forms import PollForm

from nablapps.poll.models import Poll, Choice

User = get_user_model()


class BasePollTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="gauss")
        self.question = "Hva?"
        self.form = PollForm(
            {
                "question": self.question,
                "choice_1": "un",
                "choice_2": "deux",
                "choice_3": "trois",
                "choice_4": "quatre",
            },
            user=self.user)

        self.form.is_valid()
        self.form.save()

        self.poll = Poll.objects.first()


class TestCreate(BasePollTest):

    def test_question(self):
        self.assertEqual(self.question, self.poll.question)

    def test_creator(self):
        self.assertEqual(self.user, self.poll.created_by)

    def test_is_user_poll(self):
        self.assertTrue(self.poll.is_user_poll)

    def test_not_current(self):
        self.assertFalse(self.poll.is_current)

    def test_number_of_choices(self):
        self.assertEqual(4, Choice.objects.count())


class TestUpdate(BasePollTest):

    def update_poll(self, content):
        form = PollForm(
            content,
            instance=self.poll,
            user=self.user)
        form.is_valid()
        form.save()

    def test_change_choice(self):
        self.update_poll({
            "question": self.question,
            "choice_1": "1",
            "choice_2": "1",
            "choice_3": "1",
            "choice_4": "1",
        })

        self.assertEqual(4, Choice.objects.count())
        poll = Poll.objects.first()
        for choice in poll.choices.all():
            self.assertEqual(choice.choice, "1")

    def test_delete_a_choice(self):
        self.update_poll({
            "question": self.question,
            "choice_1": "1",
            "choice_2": "2",
            "choice_3": "3",
            "choice_4": "",
        })

        self.assertEqual(3, Choice.objects.count())

    def test_delete_choice_not_at_the_end(self):
        self.update_poll({
            "question": self.question,
            "choice_1": "1",
            "choice_2": "2",
            "choice_4": "4",
        })

        self.assertEqual(3, Choice.objects.count())

    def test_delete_and_update_choice(self):
        new_choice = "yo"
        self.update_poll({
            "question": self.question,
            "choice_1": "1",
            "choice_2": "",
            "choice_3": "3",
            "choice_4": new_choice,
        })

        self.assertEqual(3, Choice.objects.count())
        self.assertTrue(Choice.objects.filter(choice=new_choice).exists())


