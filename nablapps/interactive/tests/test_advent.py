from django.test import TestCase

from nablapps.interactive.models import *


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
