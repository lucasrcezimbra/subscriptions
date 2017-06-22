import os
from datetime import date
from django.test import TestCase
from subscriptions.core.models import Import, Subscription
from subscriptions.core.validators import validate_file

from model_mommy import mommy

FILES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files')
CSV_PATH = os.path.join(FILES_PATH, 'test.csv')

class ImportModelTest(TestCase):
    fixtures = ['columns.json', 'shirt_sizes.json']

    def setUp(self):
        self.import_ = Import.objects.create(
            origin='Sprint Final',
            file=CSV_PATH
        )

    def test_new(self):
        self.assertTrue(Import.objects.exists())

    def test_delete_subscriptions_when_delete_import(self):
        mommy.make(Subscription, import_t=self.import_, _quantity=5)
        self.import_.delete()
        self.assertTrue(not Subscription.objects.exists())

    def test_subscription_has_import_id(self):
        subscription = Subscription.objects.first()
        self.assertEqual(self.import_.id, subscription.import_t.id)

    def test_import_was_successful(self):
        self.assertTrue(Subscription.objects.exists())
        self.assertTrue(Import.objects.exists())

    def test_import_correct_csv_values(self):
        self._test_first_subscription_fields()

    def test_str(self):
        self.assertEqual('Sprint Final', str(self.import_))

    def test_file_validators(self):
        self.assertEqual([validate_file],
                         Import.file.field._validators)

    def test_import_get_file_columns_names(self):
        self._create_import('test2.csv')
        self._test_first_subscription_fields()

    def test_xlsx(self):
        '''Should works with XLSX'''
        self._create_import('test.xlsx')
        self._test_first_subscription_fields()

    def test_xls(self):
        '''Should works with XLS'''
        self._create_import('test.xls')
        self._test_first_subscription_fields()

    def test_import_without_shirt_sizes(self):
        '''Should works without shirt size column'''
        self._create_import('without_shirt_size.csv')
        self._test_first_subscription_fields()

    def test_accept_formats_for_date_of_birth(self):
        '''
        12/08/1996
        12.08.1996
        '''
        self._create_import('date_format.csv', date_format='%d.%m.%Y')
        self._test_first_subscription_fields()

    def _create_import(self, filename, date_format='%d/%m/%Y', origin='Origem'):
        import_ = Import.objects.create(
            origin=origin,
            file=os.path.join(FILES_PATH, filename),
            date_format=date_format,
        )

    def _test_first_subscription_fields(self):
        fields = (
            ('name','Lucas Rangel Cezimbra 1'),
            ('email', 'lucas.cezimbra@gmail.com'),
            ('name_for_bib_number', 'Lucas 1'),
            ('gender', 'M'),
            ('date_of_birth', date(1996, 8, 12)),
            ('city', 'Porto Alegre'),
            ('team', 'Sprint Final'),
            ('shirt_size', 'BL'),
            ('modality', '1km'),
        )
        subscription = Subscription.objects.first()
        for field, expected in fields:
            with self.subTest():
                value = getattr(subscription, field)
                self.assertEqual(value, expected)
