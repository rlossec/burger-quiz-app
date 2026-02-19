# python manage.py test quiz.tests.burger_quizzes.test_detail
# GET /api/quiz/burger-quizzes/{id}/ — Détail.

import uuid

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...tests.factories import BurgerQuizFactory


class TestBurgerQuizDetailEndpoint(APITestCase):
    """GET /api/quiz/burger-quizzes/{id}/ — Détail."""

    def setUp(self):
        self.bq = BurgerQuizFactory.create(
            title="Session du 15 février 2025",
            toss="Consigne du toss.",
        )
        self.url = reverse("burger-quiz-detail", kwargs={"pk": self.bq.pk})

    # 200 OK
    def test_detail_burger_quizzes_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), str(self.bq.id))
        self.assertEqual(response.data.get("title"), self.bq.title)
        self.assertEqual(response.data.get("toss"), self.bq.toss)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)

    # 404 Not Found
    def test_detail_burger_quizzes_not_found(self):
        url = reverse("burger-quiz-detail", kwargs={"pk": uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
