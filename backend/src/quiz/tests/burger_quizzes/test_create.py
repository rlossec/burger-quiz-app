# python manage.py test quiz.tests.burger_quizzes.test_create
# POST /api/quiz/burger-quizzes/ — toss, IDs manches optionnels.

import uuid

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...models import BurgerQuiz
from ...tests.factories import (
    NuggetsFactory,
    SaltOrPepperFactory,
    MenusFactory,
    AdditionFactory,
    DeadlyBurgerFactory,
)

User = get_user_model()


class TestBurgerQuizCreateEndpoint(APITestCase):
    """POST /api/quiz/burger-quizzes/ — toss, IDs manches optionnels."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("burger-quiz-list")
        self.nuggets = NuggetsFactory.create(title="Nuggets", original=False)
        self.sop = SaltOrPepperFactory.create(title="SOP", choice_labels=["A", "B"])
        self.menus = MenusFactory.create(title="Menus", original=False)
        self.addition = AdditionFactory.create(title="Addition", original=False)
        self.deadly = DeadlyBurgerFactory.create(title="DB", original=False)
        self.valid_payload = {
            "title": "Session du 15 février 2025",
            "toss": "Description ou consigne du toss.",
            "nuggets_id": str(self.nuggets.id),
            "salt_or_pepper_id": str(self.sop.id),
            "menus_id": str(self.menus.id),
            "addition_id": str(self.addition.id),
            "deadly_burger_id": str(self.deadly.id),
        }

    # 201 Created
    def test_create_burger_quizzes_success(self):
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["title"], self.valid_payload["title"])
        self.assertEqual(response.data["toss"], self.valid_payload["toss"])
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)
        bq = BurgerQuiz.objects.get(title=self.valid_payload["title"])
        self.assertEqual(bq.nuggets_id, self.nuggets.id)
        self.assertEqual(bq.salt_or_pepper_id, self.sop.id)
        self.assertEqual(bq.menus_id, self.menus.id)
        self.assertEqual(bq.addition_id, self.addition.id)
        self.assertEqual(bq.deadly_burger_id, self.deadly.id)

    # 400 Bad Request
    def test_create_burger_quizzes_missing_toss(self):
        payload = self.valid_payload.copy()
        payload.pop("toss")
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("toss", response.data)

    def test_create_burger_quizzes_nonexistent_nuggets_id(self):
        payload = {**self.valid_payload, "nuggets_id": str(uuid.uuid4())}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 201 Created
    def test_create_with_only_toss_and_one_round(self):
        payload = {
            "title": "Quiz minimal",
            "toss": "Toss seul.",
            "nuggets_id": str(self.nuggets.id),
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["toss"], payload["toss"])
