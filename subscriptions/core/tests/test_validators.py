import os
from django.core.exceptions import ValidationError
from django.test import TestCase
from subscriptions.core.models import Import

FILES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files')
CSV_PATH = os.path.join(FILES_PATH, 'test.csv')
INVALID_COLUMNS_CSV_PATH = os.path.join(FILES_PATH, 'columns_invalid.csv')
INVALID_SHIRT_SIZES_CSV_PATH = os.path.join(FILES_PATH, 'shirt_sizes_invalid.csv')

class ValidateFileTest(TestCase):
    fixtures = ['columns.json', 'shirt_sizes.json',]
    def setUp(self):
        self.valid_import = Import(origin='Sprint Final',file=CSV_PATH)
        self.invalid_column_import = Import(
            origin='Sprint Final',
            file=INVALID_COLUMNS_CSV_PATH
        )
        self.invalid_shirt_sizes_import = Import(
            origin='Sprint Final',
            file=INVALID_SHIRT_SIZES_CSV_PATH
        )

    def test_columns_not_valid(self):
        with self.assertRaises(ValidationError):
            self.invalid_column_import.full_clean()

    def test_error_columns_not_valid(self):
        invalid_columns = ["*Nama Camplata", "Equipo"]
        expected_message = ['Colunas {} invalidas'.format(invalid_columns)]
        expected_error = str({'file': expected_message })

        with self.assertRaisesMessage(ValidationError, expected_error):
            self.invalid_column_import.full_clean()

    def test_columns_valid(self):
        self.assertIsNone(self.valid_import.full_clean())

    def test_shirt_sizes_valid(self):
        self.assertIsNone(self.valid_import.full_clean())

    def test_shirt_sizes_invalid(self):
        invalid_shirt_sizes = set(["Errado", "Inválido"])
        expected_message = ['Tamanhos de Camiseta {} invalidos'\
                            .format(invalid_shirt_sizes)]
        expected_error = str({'file': expected_message })

        with self.assertRaisesMessage(ValidationError, expected_error):
            self.invalid_shirt_sizes_import.full_clean()
