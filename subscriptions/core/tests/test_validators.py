import os
from django.core.exceptions import ValidationError
from django.test import TestCase
from subscriptions.core.models import Import

TESTS_PATH = os.path.dirname(os.path.realpath(__file__))
CSV_PATH = os.path.join(TESTS_PATH, 'test.csv')
INVALID_CSV_PATH = os.path.join(TESTS_PATH, 'columns_invalid.csv')

class ValidateFileTest(TestCase):
    fixtures = ['columns.json']
    def setUp(self):
        self.valid_import = Import(origin='Sprint Final',file=CSV_PATH)
        self.invalid_import = Import(origin='Sprint Final',file=INVALID_CSV_PATH)

    def test_columns_not_valid(self):
        with self.assertRaises(ValidationError):
            self.invalid_import.full_clean()

    def test_error_columns_not_valid(self):
        invalid_columns = ["*Nama Camplata", "Equipo"]
        expected_message = ['Colunas {} invalidas'.format(invalid_columns)]
        expected_error = str({'file': expected_message })

        with self.assertRaisesMessage(ValidationError, expected_error):
            self.invalid_import.full_clean()

    def test_columns_valid(self):
        self.assertIsNone(self.valid_import.full_clean())
