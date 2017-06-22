from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from subscriptions.core.models import ShirtSize, Subscription
from unittest import skip

from model_mommy import mommy

class ShirtSizeModelTest(TestCase):
    def setUp(self):
        self.shirt_size = mommy.prepare(ShirtSize)

    def test_create_shirt_size(self):
        self.shirt_size.save()
        self.assertTrue(ShirtSize.objects.exists())

    def test_invalid_shirt_size(self):
        shirt_size = mommy.prepare(ShirtSize, shirt_size='invalid')

        with self.assertRaises(ValidationError):
            shirt_size.save()
        self.assertFalse(ShirtSize.objects.exists())

    def test_str(self):
        self.assertEqual(self.shirt_size.shirt_size, str(self.shirt_size))
