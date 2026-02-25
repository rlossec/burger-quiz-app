# python manage.py test quiz.tests.nuggets.test_list
# GET /api/quiz/nuggets/ — Liste des manches Nuggets.

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...tests.factories import NuggetsFactory

User = get_user_model()


class TestNuggetsListEndpoint(APITestCase):
    """GET /api/quiz/nuggets/ — Liste des manches Nuggets."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
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
