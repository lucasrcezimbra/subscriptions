from django.contrib.auth.models import User
from django.test import TestCase

class ExportTest(TestCase):
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

    def login_as_staff_user(self):
        self.credentials = dict(username='admin', password='password')
        self.user = User.objects.create_user(**self.credentials, is_staff=True)
        self.client.login(**self.credentials)

    def test_html(self):
        expected_contents = (('<form', 1),
                             ('method="POST"', 1),
                             ('<input', 2),
                             ('type="submit"', 1))

        for text, count in expected_contents:
            with self.subTest():
                self.assertContains(self.response, text, count)


    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
