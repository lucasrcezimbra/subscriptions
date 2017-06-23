from collections import Counter

from subscriptions.core.models import Subscription

from django.contrib.auth.models import User
from django.test import TestCase

from model_mommy import mommy

class GetModelitiesCountTest(TestCase):
    def setUp(self):
        self.modalities = ('1','2','3','4','5','5','10','10','10')
        for modality in self.modalities:
            mommy.make('Subscription', modality=modality)

        self.login_as_staff_user()
        self.response = self.client.get('/quantidade-modalidades/')

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'count_modalities.html')

    def test_staff_member_required(self):
        self.client.logout()
        self.response = self.client.get('/quantidade-modalidades/')
        self.assertEqual(302, self.response.status_code)

    def test_context(self):
        expected = Subscription.objects.count()
        context = self.response.context['total']
        self.assertEqual(context, expected)

    def test_html(self):
        expected_contents = Counter(self.modalities)

        for value, count in expected_contents.items():
            expected = '{}: {}'.format(value, count)

            with self.subTest():
                self.assertContains(self.response, expected)

    def login_as_staff_user(self):
        self.credentials = dict(username='admin', password='password')
        self.user = User.objects.create_user(**self.credentials, is_staff=True)
        self.client.login(**self.credentials)
