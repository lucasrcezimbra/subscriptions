import os
from datetime import date
from django.test import TestCase
from subscriptions.core.models import Import,Subscription

TESTS_PATH = os.path.dirname(os.path.realpath(__file__))
CSV_PATH = os.path.join(TESTS_PATH, 'test.csv')

class ImportModelTest(TestCase):
    def setUp(self):
        self.import_ = Import.objects.create(
            origin='Sprint Final',
            file=CSV_PATH
        )

    def test_new(self):
        self.assertTrue(Import.objects.exists())

    def test_delete_subscriptions_when_delete_import(self):
        for i in range(5):
            Subscription.objects.create(
                name='Lucas Rangel Cezimbra',
                email='lucas.cezimbra@gmail.com',
                name_for_bib_number='Lucas',
                gender='M',
                date_of_birth='1996-08-12',
                city='Porto Alegre',
                team='Sprint Final',
                shirt_size='P',
                modality='5km',
                import_t=self.import_,
            )

        self.import_.delete()
        self.assertTrue(not Subscription.objects.exists())

    def test_subscription_has_import_id(self):
        subscription = Subscription.objects.first()
        self.assertEqual(self.import_.id, subscription.import_t.id)

    def test_import_was_successful(self):
        self.assertTrue(Subscription.objects.exists())
        self.assertTrue(Import.objects.exists())

    def test_import_correct_csv_values(self):
        fields = (
            ('name','Lucas Rangel Cezimbra 1'),
            ('email', 'lucas.cezimbra@gmail.com'),
            ('name_for_bib_number', 'Lucas 1'),
            ('gender', 'M'),
            ('date_of_birth', date(1996, 8, 12)),
            ('city', 'Porto Alegre'),
            ('team', 'Sprint Final'),
            ('shirt_size', 'P'),
            ('modality', '1km'),
        )
        subscription = Subscription.objects.first()
        for field, expected in fields:
            with self.subTest():
                value = getattr(subscription, field)
                self.assertEqual(value, expected)

    def test_str(self):
        self.assertEqual('1', str(self.import_))
