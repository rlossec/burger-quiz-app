# python manage.py test quiz.tests.nuggets.test_list
# GET /api/quiz/nuggets/ — Liste des manches Nuggets.

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...tests.factories import NuggetsFactory


class TestNuggetsListEndpoint(APITestCase):
    """GET /api/quiz/nuggets/ — Liste des manches Nuggets."""

    def setUp(self):
        self.url = reverse("nuggets-list")
        self.nuggets = NuggetsFactory.create(title="Culture générale", original=False)

    def test_list_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_exposes_original_and_questions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data.get("results", response.data)
        if data:
            self.assertIn("original", data[0])
            self.assertIn("title", data[0])
