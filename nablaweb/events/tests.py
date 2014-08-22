from django.test import TestCase
from django.contrib.auth import get_user_model; User = get_user_model()
from events.models import Event
import datetime
import random

class WaitingListTest(TestCase):
    def setUp(self):
        # Lag en bruker som kan "lage" arrangementet
        self.user = User.objects.create(username='oyvinlek', password='oyvinlek')

        # Opprett et arrangement
        self.event = Event.objects.create(
            created_by=self.user,
            location="Here",
            headline="Title",
            lead_paragraph="Text.",
            body="More text.",
            event_start=datetime.datetime(2030,1,1),
            registration_deadline=datetime.datetime(2029,1,1),
            places=10,
            has_queue=True,
            )
        self.event.test_event_fields()

        # Lag og registrer noen brukere
        self.event.register_user(self.user)
        for i in xrange(1, 20):
            u = User.objects.create(username='user%d'%i, password='user%d'%i)
            self.event.register_user(u)

    def test_ordering(self):
        user_regs = self.event.eventregistration_set.all().order_by('number')
        regs = len(user_regs)
        for reg, i in zip(user_regs, xrange(1, regs+1)):
            self.assertEqual(reg.number, i)

    def test_move_to_top(self):
        first = 1
        for user in User.objects.all():
            self.event.move_user_to_place(user, first)
            reg = self.event.eventregistration_set.get(user=user)
            self.assertEqual(reg.number, first)
            self.test_ordering()

    def test_move_to_end(self):
        last = self.event.eventregistration_set.count()
        for user in User.objects.all():
            self.event.move_user_to_place(user, last)
            reg = self.event.eventregistration_set.get(user=user)
            self.assertEqual(reg.number, last)
            self.test_ordering()

    def test_move_past_top(self):
        first = 1
        for user in User.objects.all():
            self.event.move_user_to_place(user, first-1)
            reg = self.event.eventregistration_set.get(user=user)
            self.assertEqual(reg.number, first)
            self.test_ordering()
            self.event.move_user_to_place(user, first-100)
            reg = self.event.eventregistration_set.get(user=user)
            self.assertEqual(reg.number, first)
            self.test_ordering()

    def test_move_past_end(self):
        last = self.event.eventregistration_set.count()
        for user in User.objects.all():
            self.event.move_user_to_place(user, last+1)
            reg = self.event.eventregistration_set.get(user=user)
            self.assertEqual(reg.number, last)
            self.test_ordering()
            self.event.move_user_to_place(user, last+100)
            reg = self.event.eventregistration_set.get(user=user)
            self.assertEqual(reg.number, last)
            self.test_ordering()

    def test_move_one_up(self):
        first = 1
        for user in User.objects.all():
            reg = self.event.eventregistration_set.get(user=user)
            self.event.move_user_to_place(user, reg.number-1)
            self.test_ordering()

    def test_move_one_down(self):
        last = self.event.eventregistration_set.count()
        for user in User.objects.all():
            reg = self.event.eventregistration_set.get(user=user)
            self.event.move_user_to_place(user, reg.number+1)
            self.test_ordering()

    def test_random_moves(self):
        regs = self.event.eventregistration_set.count()
        for i in xrange(regs):
            reg = random.choice(self.event.eventregistration_set.all())
            user = reg.user
            place = random.randint(1, regs)
            self.event.move_user_to_place(user, place)
            reg = self.event.eventregistration_set.get(user=user)
            self.assertEqual(reg.number, place)
            self.test_ordering()

    def test_deregister_user(self):
        while self.event.users_registered() != 0:
            reg = random.choice(self.event.eventregistration_set.all())
            user = reg.user
            self.event.deregister_user(user)
            self.test_ordering()
