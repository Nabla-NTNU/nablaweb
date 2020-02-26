from datetime import date

from django.test import Client, TestCase
from django.urls import reverse

from nablapps.accounts.models import NablaUser


class BirthdayTest(TestCase):
    def setUp(self):
        self.users = [NablaUser.objects.create(username=f"user{i}") for i in range(10)]
        self.birthday_today = self.users[::2]
        self.set_birthday_today(self.birthday_today)

    def test_filter_birthday_today(self):
        self.assertListEqual(
            list(NablaUser.objects.filter_has_birthday_today()), self.birthday_today
        )

    def set_birthday_today(self, user_list):
        today = date.today()
        for year, user in enumerate(user_list, start=1990):
            user.birthday = date(year=year, month=today.month, day=today.day)
            user.save()

    def test_view(self):

        c = get_client_with_logged_in_user()
        response = c.get(reverse("users_birthday"))

        text = response.content.decode()
        for user in self.birthday_today:
            name = user.first_name
            self.assertIn(name, text)


def get_client_with_logged_in_user():
    user = NablaUser.objects.first()
    password = "asfasdfjaskdlfjsadfk"
    user.set_password(password)
    c = Client()
    c.login(username=user.username, password=password)
    return c
