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
