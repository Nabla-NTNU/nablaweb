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
                "solution": code,
                "output": output or self.correct_output,
            },
        )

        self.task.refresh_from_db()

    def test_submit_code(self):
        code_0 = "print(2)"
        code_1 = "# comment\r\nprint(1)\r\n"
        code_2 = "print(1)\r\n"
        code_3 = "print(1)\n"

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
            self.task.result_set.first().length, Result.solution_length(code_1)
        )

        # Move the old submission back a day to prevent flakyness of the test
        old_submission = self.task.result_set.first()
        old_submission.submitted_at -= timedelta(days=1)
        old_submission.save()

        last_submitted_at = self.task.result_set.first().submitted_at

        # Submit better code
        self.submit_code(code_2)

        self.assertEqual(
            self.task.result_set.count(),
            2,
            "A new solution should be added.",
        )
        self.assertEqual(
            self.task.result_set.first().length, Result.solution_length(code_2)
        )
        new_submitted_at = self.task.result_set.first().submitted_at

        self.assertNotEqual(
            last_submitted_at,
            new_submitted_at,
            "The submitted at timestamp should be updated as the user submitted a new solution",
        )

        self.assertEqual(
            self.task.result_set.first().length, Result.solution_length(code_2)
        )

        self.submit_code(code_3)
        self.assertEqual(
            self.task.result_set.first().length,
            self.task.result_set.all()[1].length,
            "There should be no difference between using \r\n and \n",
        )

    def test_view_score(self):
        url = reverse("code_golf_score", kwargs={"task_id": self.task.id})
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200,
            "View should return ok when user has not submitted",
        )

        self.submit_code("print(1)")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 200, "View should return ok when user has submitted"
        )

        self.task.delete()
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            404,
            "View should return not found when task doesn't exist",
        )

        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            302,
            "View should redirect to login when user is logged out",
        )
