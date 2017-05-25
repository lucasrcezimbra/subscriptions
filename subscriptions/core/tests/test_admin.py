from django.contrib import admin
from django.test import TestCase
from subscriptions.core.admin import ColumnModelAdmin, ImportModelAdmin, SubscriptionModelAdmin
from subscriptions.core.models import Column,Import,Subscription
from unittest.mock import Mock

class SubscriptionModelAdminTest(TestCase):
    def setUp(self):
        self.model_admin = SubscriptionModelAdmin(Subscription, admin.site)

    def test_model_admin(self):
        self.assertIsInstance(self.model_admin, SubscriptionModelAdmin)

    def test_is_registered_in_admin(self):
        self.assertTrue(admin.site.is_registered(Subscription))
        self.assertIsInstance(admin.site._registry[Subscription],
                              SubscriptionModelAdmin)

    def test_attr(self):
        attrs = [
            ('list_display', ('name', 'email', 'gender', 'date_of_birth', 'city', 'team', 'shirt_size', 'modality', 'import_'))
        ]

        for attr, expected in attrs:
            with self.subTest():
                self.assertEqual(expected, getattr(self.model_admin, attr))

    def test_import_(self):
        mock = Mock(import_t=5)
        import_ = self.model_admin.import_
        self.assertEqual(5, import_(mock))
        self.assertEqual('Import ID', import_.short_description)

class ImportModelAdminTest(TestCase):
    def setUp(self):
        self.model_admin = ImportModelAdmin(Import, admin.site)

    def test_model_admin(self):
        self.assertIsInstance(self.model_admin, ImportModelAdmin)

    def test_is_registered_in_admin(self):
        self.assertTrue(admin.site.is_registered(Import))
        self.assertIsInstance(admin.site._registry[Import],
                              ImportModelAdmin)

    def test_attr(self):
        attrs = [
            ('list_display', ('pk','origin',))
        ]

        for attr, expected in attrs:
            with self.subTest():
                self.assertEqual(expected, getattr(self.model_admin, attr))


class ColumnModelAdminTest(TestCase):
    def setUp(self):
        self.model_admin = ColumnModelAdmin(Column, admin.site)

    def test_model_admin(self):
        self.assertIsInstance(self.model_admin, ColumnModelAdmin)

    def test_is_registered_in_admin(self):
        self.assertTrue(admin.site.is_registered(Column))
        self.assertIsInstance(admin.site._registry[Column],
                              ColumnModelAdmin)

    def test_attr(self):
        attrs = [
            ('list_display', ('column_name', 'id',)),
        ]

        for attr, expected in attrs:
            with self.subTest():
                self.assertEqual(expected, getattr(self.model_admin, attr))
