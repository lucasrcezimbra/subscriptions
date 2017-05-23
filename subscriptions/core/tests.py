import os
from django.test import TestCase
from subscriptions.core.models import Subscription

class SubscriptionTest(TestCase):
    def test_create(self):
        subscription = Subscription.objects.create(
            name='Lucas Rangel Cezimbra',
            email='lucas.cezimbra@gmail.com',
            name_for_bib_number='Lucas',
            gender='M',
            date_of_birth='1996-08-12',
            city='Porto Alegre',
            team='Sprint Final',
            shirt_size='P',
            modality='5km',
        )

    def test_fields_can_be_blank(self):
        fields_can_be_blank = ('name_for_bib_number', 'city', 'team')

        for field_name in fields_can_be_blank:
            with self.subTest():
                field = Subscription._meta.get_field(field_name)
                self.assertTrue(field.blank)


class ImportViewTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/import/')

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_return_import_template(self):
        self.assertTemplateUsed(self.response, 'import.html')

    def test_html_contains(self):
        tags = (
            ('<form', 1),
            ('<input', 3),
            ('type="submit"', 1),
        )

        for tag,count in tags:
            with self.subTest():
                self.assertContains(self.response, tag, count)

    def test_contains_crsf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

class ImportViewPostTest(TestCase):
    def setUp(self):
        self.TESTS_PATH = os.path.dirname(os.path.realpath(__file__))
        with open(self.TESTS_PATH + '/test.csv') as file:
            self.response = self.client.post('/import/', {'file': file})

    def test_post(self):
        self.assertEqual(200, self.response.status_code)
