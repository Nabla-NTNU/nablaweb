from datetime import datetime, timedelta
from random import random

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from nablapps.interactive.models.code_golf import CodeTask, Result

User = get_user_model()


class CodeGolfTests(TestCase):
    def setUp(self):
        # Create a task
        self.correct_output = "1"
        self.task = CodeTask.objects.create(
            title="My code task", task="Compute 1", correct_output=self.correct_output
        )

        # Create a user to log in as
        username = password = "golfer"
        User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)

    def submit_code(self, code, output=None):
        """Submit the code by posting to the endpoint"""
        self.client.post(
            reverse("code_golf", kwargs={"task_id": self.task.id}),
            data={
                "submitted_code": code,
                "submitted_output": output or self.correct_output,
            },
        )

        self.task.refresh_from_db()

    def test_submit_code(self):
        code_0 = "print(2)"
        code_1 = "# comment\r\nprint(1)\r\n"
        code_2 = "print(1)\r\n"

        self.assertEqual(
            self.task.result_set.count(),
            0,
            "A newly created task should have no submissions",
        )

        # Submit bad code
        self.submit_code(code_0, output="2\n")

        self.assertEqual(
            self.task.result_set.count(),
            0,
            "A new result should not be created when the user fails",
        )

        # Submit working code
        self.submit_code(code_1)

        self.assertEqual(
            self.task.result_set.count(),
            1,
            "The task should have one submission after the user submitted",
        )
        self.assertEqual(
            self.task.result_set.first().length, Result.compute_length(code_1)
        )
        last_submitted_at = self.task.result_set.first().submitted_at

        # Submit better code
        self.submit_code(code_2)

        self.assertEqual(
            self.task.result_set.count(),
            1,
            "The user's submission should be overridden, and a new one should not be created",
        )
        self.assertEqual(
            self.task.result_set.first().length, Result.compute_length(code_2)
        )
        new_submitted_at = self.task.result_set.first().submitted_at

        self.assertNotEqual(
            last_submitted_at,
            new_submitted_at,
            "The submitted at timestamp should be updated as the user got a better score",
        )

        # Submit worse code
        self.submit_code(code_1)
        newest_submitted_at = self.task.result_set.first().submitted_at
        self.assertEqual(
            newest_submitted_at,
            new_submitted_at,
            "The submitted at timestamp should not be updated as the user got a worse score",
        )

        self.assertEqual(
            self.task.result_set.first().length, Result.compute_length(code_2)
        )
