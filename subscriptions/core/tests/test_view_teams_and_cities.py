from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.test import TestCase


class GetTeamCitisTest(TestCase):
    fixtures = ['subscriptions.json',]
    def setUp(self):
        self.login_as_staff_user()
        self.response = self.client.get('/cidades-equipes/')

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_staff_member_required(self):
        self.client.logout()
        self.response = self.client.get('/cidades-equipes/')
        self.assertEqual(302, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'teams_cities.html')

    def test_context(self):
        teams = self.response.context['teams']
        cities = self.response.context['cities']
        self.assertIsInstance(teams, QuerySet)
        self.assertIsInstance(cities, QuerySet)

        expected_team = ('Sprint Final', 3)
        expected_city = ('Canoas', 2)
        self.assertEqual(teams[0], expected_team)
        self.assertEqual(cities[0], expected_city)

    def test_html(self):
        expected_contents = (
            ('Cidades', 1),
            ('Equipes', 1),
            ('Porto Alegre', 1),
            ('3', 1),
            ('Canoas', 1),
            ('2', 2),
            ('Sprint Final', 1),
            ('Equipen', 1)
        )
        for expected, count in expected_contents:
            with self.subTest():
                self.assertContains(self.response, expected, count)

    def test_cities_must_be_ordered(self):
        cities = self.response.context['cities']
        sorted_cities = sorted(cities, key=lambda d: d[1], reverse=True)
        self.assertEqual(list(cities), sorted_cities)

    def test_teams_must_be_ordered(self):
        teams = self.response.context['teams']
        sorted_teams = sorted(teams, key=lambda d: d[1], reverse=True)
        self.assertEqual(list(teams), sorted_teams)

    def login_as_staff_user(self):
        self.credentials = dict(username='admin', password='password')
        self.user = User.objects.create_user(**self.credentials, is_staff=True)
        self.client.login(**self.credentials)
