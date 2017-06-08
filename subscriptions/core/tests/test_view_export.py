from django.contrib.auth.models import User
from django.test import TestCase
from subscriptions.core.forms import ExportForm

class GetExportTest(TestCase):
    def setUp(self):
        self.login_as_staff_user()
        self.response = self.client.get('/export/')

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'export.html')

    def test_staff_member_required(self):
        self.client.logout()
        self.response = self.client.get('/export/')
        self.assertEqual(302, self.response.status_code)

    def test_html(self):
        expected_contents = (('<form', 1),
                             ('method="POST"', 1),
                             ('<input', 3),
                             ('type="submit"', 1),
                             ('type="radio"', 1),
                             ('<select', 1))

        for text, count in expected_contents:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_context(self):
        expected = (('form', ExportForm),)

        for value, type in expected:
            with self.subTest():
                context = self.response.context[value]
                self.assertIsInstance(context, type)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def login_as_staff_user(self):
        self.credentials = dict(username='admin', password='password')
        self.user = User.objects.create_user(**self.credentials, is_staff=True)
        self.client.login(**self.credentials)

class PostExportTest(TestCase):
    def setUp(self):
        self.login_as_staff_user()
        self.data = dict(format='csv', fields=['id', 'name', 'email'])
        self.response = self.client.post('/export/', self.data)

    def test_post(self):
        self.assertEqual(200, self.response.status_code)

    def test_staff_member_required(self):
        self.client.logout()
        self.response = self.client.post('/export/', self.data)
        self.assertEqual(302, self.response.status_code)

    def test_response_content_type_is_csv(self):
        content_type = 'text/csv'
        self.assertEquals(content_type, self.response.get('Content-Type'))

    def test_content_is_not_none(self):
        self.assertTrue(self.response.content)

    def test_file_is_csv(self):
        extension = self.response.get('Content-Disposition').split('.')[-1]
        self.assertEqual('csv', extension)

    def login_as_staff_user(self):
        self.credentials = dict(username='admin', password='password')
        self.user = User.objects.create_user(**self.credentials, is_staff=True)
        self.client.login(**self.credentials)
