from datetime import datetime, timedelta
from random import random

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from nablapps.interactive.models.quiz import (
    QuestionReply,
    Quiz,
    QuizQuestion,
    QuizReply,
    QuizReplyTimeout,
)

User = get_user_model()


class BaseQuizTest(TestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(title="Test quiz", is_timed=True, duration=100)
        self.questions = []
        for i in range(1, 24):
            question = QuizQuestion.objects.create(
                question="Something?",
                correct_alternative=1,
                alternative_1="One",
                alternative_2="Two",
                alternative_3="Three",
                alternative_4="Four",
                quiz=self.quiz,
            )
            self.questions.append(question)


class QuizTests(BaseQuizTest):
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
        data = {f"{q.id}_alternative": int(random() * 4 + 1) for q in self.questions}
        self.client.post(reverse("quiz_reply", kwargs={"pk": self.quiz.id}), data=data)


class QuizReplyTest(BaseQuizTest):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(username="quizlover")
        self.reply = QuizReply.objects.create(
            user=self.user,
            scoreboard=self.quiz.scoreboard,
            start=datetime.now(),
            when=datetime.now(),
        )

    def test_add_question_replies(self):
        replies = [(q, q.correct_alternative) for q in self.questions]
        self.reply.add_question_replies(replies)
        self.assertEqual(
            self.reply.get_correct_count(), self.reply.get_question_count()
        )

    def test_add_question_replies_raises_exception_on_timeout(self):
        self.quiz.duration = 1
        self.quiz.save()
        self.reply.start = datetime.now() - timedelta(seconds=3600)
        with self.assertRaises(QuizReplyTimeout):
            self.reply.add_question_replies([])

    def test_only_possible_to_have_one_answer_per_question(self):
        replies = [(q, q.correct_alternative) for q in self.questions]
        self.reply.add_question_replies(replies)
        self.reply.add_question_replies(replies)
        self.assertEqual(
            len(replies), QuestionReply.objects.filter(quiz_reply=self.reply).count()
        )
