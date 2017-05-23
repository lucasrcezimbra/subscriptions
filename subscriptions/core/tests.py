from django.test import TestCase
from subscriptions.core.models import Subscription

class SubscriptionTest(TestCase):
    def test_name_not_blank(self):
        subscription = Subscription.objects.create(
            name='Lucas Rangel Cezimbra',
            email='lucas.cezimbra@gmail.com',
            name_for_bib_number='lucas.cezimbra@gmail.com',
            gender='M',
            date_of_birth='1996-08-12',
            city='Porto Alegre',
            team='Sprint Final',
        )
