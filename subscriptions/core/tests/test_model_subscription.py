from django.core.exceptions import ValidationError
from django.test import TestCase
from model_mommy import mommy

from subscriptions.core.models import ShirtSize, Subscription


class SubscriptionTest(TestCase):
    def setUp(self):
        self.subscription = mommy.prepare(Subscription)

    def test_create(self):
        self.subscription.save()
        self.assertTrue(Subscription.objects.exists())

    def test_fields_can_be_blank(self):
        fields_can_be_blank = ('email', 'name_for_bib_number', 'city', 'team')

        for field_name in fields_can_be_blank:
            with self.subTest():
                field = Subscription._meta.get_field(field_name)
                self.assertTrue(field.blank)

    def test_invalid_shirt_size(self):
        self.subscription.shirt_size = 'INVALID'
        with self.assertRaises(ValidationError):
            self.subscription.save()
        self.assertFalse(Subscription.objects.exists())

    def test_invalid_modality_choice(self):
        self.subscription.modality = 'INVALID'
        with self.assertRaises(ValidationError):
            self.subscription.save()
        self.assertFalse(Subscription.objects.exists())

    def test_str(self):
        self.assertEqual(self.subscription.name, str(self.subscription))
