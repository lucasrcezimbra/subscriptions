from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from subscriptions.core.models import ShirtSize, Subscription
from unittest import skip

class ShirtSizeModelTest(TestCase):
    def setUp(self):
        self.shirt_size = ShirtSize(
            shirt_size='P',
            file_shirt_size='Camiseta P',
        )

    def test_create_shirt_size(self):
        self.shirt_size.save()
        self.assertTrue(ShirtSize.objects.exists())

    @skip('Validation not implemented')
    def test_invalid_shirt_size(self):
        shirt_size = ShirtSize(
            shirt_size='invalid_shirt_size',
            file_shirt_size='Camiseta P',
        )
        with self.assertRaises(ValidationError):
            shirt_size.save()
        self.assertFalse(ShirtSize.objects.exists())

    def test_str(self):
        self.assertEqual('P', str(self.shirt_size))

    def test_dont_delete_subscriptions_when_delete_shirt_size(self):
        shirt_size,_ = ShirtSize.objects.get_or_create(
            shirt_size='P',
            file_shirt_size='Camiseta P',
        )
        for i in range(5):
            Subscription.objects.create(
                name='Lucas Rangel Cezimbra',
                email='lucas.cezimbra@gmail.com',
                name_for_bib_number='Lucas',
                gender='M',
                date_of_birth='1996-08-12',
                city='Porto Alegre',
                team='Sprint Final',
                shirt_size=shirt_size,
                modality='5km',
            )

        with self.assertRaises(ProtectedError):
            self.shirt_size.delete()

        self.assertTrue(Subscription.objects.exists())
