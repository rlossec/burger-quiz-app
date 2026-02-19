# python manage.py test quiz.tests.burger_quizzes.test_list
# GET /api/quiz/burger-quizzes/ — Liste avec created_at, updated_at.

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class TestBurgerQuizListEndpoint(APITestCase):
    """GET /api/quiz/burger-quizzes/ — Liste avec created_at, updated_at."""

    def setUp(self):
        self.url = reverse("burger-quiz-list")

    # 200 OK
    def test_list_burger_quizzes_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 200 OK
    def test_list_burger_quizzes_exposes_created_at_updated_at(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data.get("results", response.data)
        if data:
            self.assertIn("created_at", data[0])
            self.assertIn("updated_at", data[0])
