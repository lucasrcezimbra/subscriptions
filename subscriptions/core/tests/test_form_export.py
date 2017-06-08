from django.test import TestCase
from subscriptions.core.forms import ExportForm
from subscriptions.core.models import Subscription

class ExportFormTest(TestCase):
    def setUp(self):
        self.form = ExportForm()

    def test_formats(self):
        self.assertIn(('csv', 'CSV'), self.form.FORMATS)
        self.assertIn(('xlsx', 'XLSX'), self.form.FORMATS)

    def test_has_fields(self):
        expected = ['format', 'fields']
        self.assertSequenceEqual(expected, list(self.form.fields))

    def test_format_has_choices(self):
        self.assertEqual(self.form.fields['format'].choices,
                         list(self.form.FORMATS))

    def test_fields(self):
        expected = [(field.name, field.verbose_name)
                    for field in Subscription._meta.get_fields()]
        self.assertEqual(expected, self.form.FIELDS)

    def test_fields_has_choices(self):
        self.assertEqual(self.form.fields['fields'].choices,
                         list(self.form.FIELDS))
