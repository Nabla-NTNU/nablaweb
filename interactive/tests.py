from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import *
from random import random


class AdventTests(TestCase):
    def setUp(self):
        self.cal = AdventCalendar.objects.create(
            year=2015
        )
        self.doors = []
        for i in range(1, 24):
            door = AdventDoor.objects.create(
                template="interactive/advent_door_base.html",
                content="Test",
                number=i,
                calendar=self.cal
            )
            self.doors.append(door)

    def test_update(self):
        for d in self.doors:
            d.content = "Hello world"
            d.save()

        self.cal.year += 1
        self.cal.save()

    def test_delete(self):
        for d in self.doors:
            d.delete()

        self.cal.delete()


class QuizTests(TestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(
            title="Test quiz",
            is_timed=True,
            duration=100
        )
        self.questions = []
        for i in range(1, 24):
            question = QuizQuestion.objects.create(
                question="Something?",
                correct_alternative=1,
                alternative_1="One",
                alternative_2="Two",
                alternative_3="Three",
                alternative_4="Four",
                quiz=self.quiz
            )
            self.questions.append(question)

    def test_update(self):
        for q in self.questions:
            q.question = "Hello world?"
            q.save()

        self.quiz.save()

    def test_delete(self):
        for d in self.questions:
            d.delete()

        self.quiz.delete()

    def test_reply(self):
        data = {'{id}_alternative'.format(id=q.id): int(random() * 4 + 1) for q in self.questions}
        self.client.post(reverse('quiz_reply', kwargs={'pk': self.quiz.id}), data=data)
