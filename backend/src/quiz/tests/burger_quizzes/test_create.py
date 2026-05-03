# python manage.py test quiz.tests.burger_quizzes.test_create
# POST /api/quiz/burger-quizzes/ — titre, toss.

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...models import BurgerQuiz

User = get_user_model()


class TestBurgerQuizCreateEndpoint(APITestCase):
    """POST /api/quiz/burger-quizzes/ — titre et toss obligatoires ; structure via PUT séparé."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("burger-quiz-list")
        self.valid_payload = {
            "title": "Session du 15 février 2025",
            "toss": "Description ou consigne du toss.",
        }

    def test_create_burger_quizzes_success(self):
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["title"], self.valid_payload["title"])
        self.assertEqual(response.data["toss"], self.valid_payload["toss"])
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)
        bq = BurgerQuiz.objects.get(title=self.valid_payload["title"])
        self.assertEqual(bq.structure_elements.count(), 0)

    def test_create_burger_quizzes_missing_toss(self):
        payload = self.valid_payload.copy()
        payload.pop("toss")
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("toss", response.data)
