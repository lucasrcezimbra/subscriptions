from django.core.exceptions import ValidationError
from django.test import TestCase
from subscriptions.core.models import Column

class ColumnTest(TestCase):
    def setUp(self):
        self.column = Column(
            column_name='name',
            id='*Nome Completo',
        )

    def test_create(self):
        self.column.save()
        self.assertTrue(Column.objects.exists())

    def test_invalid_column_name(self):
        column = Column(
            column_name='invalid_column',
            id='*Nome Completo',
        )
        with self.assertRaises(ValidationError):
            column.save()
        self.assertFalse(Column.objects.exists())

    def test_str(self):
        self.assertEqual('*Nome Completo', str(self.column))
