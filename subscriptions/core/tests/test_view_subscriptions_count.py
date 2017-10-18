import os
from collections import namedtuple
from unittest.mock import patch

from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.test import TestCase
from model_mommy import mommy

from subscriptions.core.models import Import, Subscription


FILES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files')
CSV_PATH = os.path.join(FILES_PATH, 'test.csv')


class GetSubscriptionsCountTest(TestCase):
    fixtures = ['columns.json', 'modalities.json', 'shirt_sizes.json']

    @patch('subscriptions.core.views.Sympla')
    def setUp(self, SymplaMock):
        SymplaMock._authenticate.return_value = None
        Event = namedtuple('Event', ['confirmed_participants', 'pending_participants'])
        self.event = Event('5', '10')
        SymplaMock().get_event.return_value = self.event

        import_ = Import.objects.create(
            origin='Sprint Final',
            file=CSV_PATH
        )
        self.without_imports_quantity = 10
        mommy.make(Subscription, _quantity=self.without_imports_quantity)

        self.login_as_staff_user()
        self.response = self.client.get('/quantidade-inscritos/')

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_staff_member_required(self):
        self.client.logout()
        self.response = self.client.get('/quantidade-inscritos/')
        self.assertEqual(302, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'count.html')

    def test_context_imports_count(self):
        context = self.response.context['counter']
        self.assertIsInstance(context, QuerySet)

    def test_context_without_import_count(self):
        context = self.response.context['alone']
        self.assertEqual(context, self.without_imports_quantity)

    def test_context_total(self):
        sympla_count = int(self.event.confirmed_participants) + int(self.event.pending_participants)
        expected_total = Subscription.objects.count() + sympla_count
        total = self.response.context['total']
        self.assertEqual(total, expected_total)

    def test_context_sympla(self):
        sympla = self.response.context['extra']
        expected = {
            'sympla confirmados': int(self.event.confirmed_participants),
            'sympla pendentes': int(self.event.pending_participants),
        }
        self.assertEqual(sympla, expected)

    def test_html(self):
        expected_contents = (
            'Sprint Final: 5',
            'Avulso: {}'.format(self.without_imports_quantity),
            'Total: 30',
            'Sympla Confirmados: {}'.format(self.event.confirmed_participants),
            'Sympla Pendentes: {}'.format(self.event.pending_participants),
        )
        for expected in expected_contents:
            with self.subTest():
                self.assertContains(self.response, expected)

    @patch('subscriptions.core.views.Sympla')
    def test_html_if_dont_have_without_import(self, SymplaMock):
        SymplaMock._authenticate.return_value = None
        Subscription.objects.all().delete()
        self.response = self.client.get('/quantidade-inscritos/')
        self.assertNotContains(self.response, 'Avulso: 0')

    def login_as_staff_user(self):
        self.credentials = dict(username='admin', password='password')
        self.user = User.objects.create_user(**self.credentials, is_staff=True)
        self.client.login(**self.credentials)
