from django.core.exceptions import ValidationError
from django.test import TestCase
from model_mommy import mommy

from subscriptions.core.models import Column


class ColumnTest(TestCase):
    def setUp(self):
        self.column = mommy.prepare(Column)

    def test_create(self):
        self.column.save()
        self.assertTrue(Column.objects.exists())

    def test_invalid_column_name(self):
        column = mommy.prepare(Column, subscription_name='invalid_column')

        with self.assertRaises(ValidationError):
            column.save()
        self.assertFalse(Column.objects.exists())

    def test_str(self):
        self.assertEqual(self.column.file_column, str(self.column))
