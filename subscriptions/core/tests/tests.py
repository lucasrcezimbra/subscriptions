import os
from datetime import date
from django.test import TestCase
from subscriptions.core.models import Import,Subscription
from subscriptions.core.helpers import SubscriptionImporter
from unittest import skip

TESTS_PATH = os.path.dirname(os.path.realpath(__file__))

class SubscriptionTest(TestCase):
    def test_create(self):
        subscription = Subscription.objects.create(
            name='Lucas Rangel Cezimbra',
            email='lucas.cezimbra@gmail.com',
            name_for_bib_number='Lucas',
            gender='M',
            date_of_birth='1996-08-12',
            city='Porto Alegre',
            team='Sprint Final',
            shirt_size='P',
            modality='5km',
        )

    def test_fields_can_be_blank(self):
        fields_can_be_blank = ('name_for_bib_number', 'city', 'team')

        for field_name in fields_can_be_blank:
            with self.subTest():
                field = Subscription._meta.get_field(field_name)
                self.assertTrue(field.blank)


class SubscriptionImporterHelperTest(TestCase):
    def setUp(self):
        filepath = TESTS_PATH + '/test.csv'
        self.importer = SubscriptionImporter(filepath)
        self.importer.save()

    def test_new(self):
        self.assertIsInstance(self.importer, SubscriptionImporter)

    @skip('Fix')
    def test_import(self):
        self.assertTrue(Subscription.objects.exists())
        self.assertTrue(Import.objects.exists())

    def test_fields_imported(self):
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

class ImportModelTest(TestCase):
    def setUp(self):
        filepath = TESTS_PATH + '/test.csv'
        self.import_ = Import.objects.create(
            file=filepath
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
