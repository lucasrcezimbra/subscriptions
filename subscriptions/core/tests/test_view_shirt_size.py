from django.contrib.auth.models import User
from django.test import TestCase

class GetExportTest(TestCase):
    fixtures = ['subscriptions']

    def setUp(self):
        self.login_as_staff_user()
        self.response = self.client.get('/camisetas/')

    def test_template(self):
        self.assertTemplateUsed(self.response, 'shirt_sizes.html')

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_staff_member_required(self):
        self.client.logout()
        self.response = self.client.get('/camisetas/')
        self.assertEqual(302, self.response.status_code)

    def test_html(self):
        expected_contents = ('P: 1',
                             'M: 1',
                             'G: 1',
                             'GG: 1',
                             'BL: 1')

        for expected in expected_contents:
            with self.subTest():
                self.assertContains(self.response, expected)

    def login_as_staff_user(self):
        self.credentials = dict(username='admin', password='password')
        self.user = User.objects.create_user(**self.credentials, is_staff=True)
        self.client.login(**self.credentials)
