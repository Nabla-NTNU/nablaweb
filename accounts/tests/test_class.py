from datetime import date
from django.test import TestCase

from accounts.models import NablaUser, FysmatClass


class ClassesTest(TestCase):
    def setUp(self):
        now = date.today()
        years = [now.year - y for y in range(7)]
        self.classes = [
            FysmatClass.objects.create(
                name="kull{}".format(year),
                starting_year=year 
            ) for year in years
        ]
        self.users = []

        for j, cls in enumerate(self.classes):
            users = [
                NablaUser.objects.create(
                    username="user{}".format(j*10+i)
                ) for i in range(4)
            ]
            
            for u in users:
                cls.user_set.add(u)
            self.users += users 
            
    def test_user_class(self):
        for i in range(28):
            cls = self.classes[int(i/7)]
            u = self.users[i]
            assert u.get_class_number() <= 5
            
