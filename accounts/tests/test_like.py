from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from accounts.models import NablaUser, LikePress

class TestLikeModel(TestCase):
    def setUp(self):
        self.user = NablaUser.objects.create(username="narcissus")

    def test_toggle(self):
        LikePress.objects.create_or_delete(
            user=self.user,
            model_name=ContentType.objects.get_for_model(NablaUser).model,
            reference_id=self.user.id
        )
        self.assertTrue(LikePress.objects.exists())

        LikePress.objects.create_or_delete(
            user=self.user,
            model_name=ContentType.objects.get_for_model(NablaUser).model,
            reference_id=self.user.id
        )
        self.assertFalse(LikePress.objects.exists())
