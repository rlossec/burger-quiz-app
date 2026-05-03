# python manage.py test quiz.tests.deadly_burgers.test_create
# POST /api/quiz/deadly-burgers/ — Exactement 10 questions, type DB.

import uuid

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...models import DeadlyBurger
from ...tests.factories import QuestionFactory

User = get_user_model()


class TestDeadlyBurgerCreateEndpoint(APITestCase):
    """POST /api/quiz/deadly-burgers/ — Exactement 10 questions, type DB."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("deadly-burger-list")
        self.questions = [QuestionFactory.create_db(f"DB{i}") for i in range(1, 11)]
        self.valid_payload = {
            "title": "Burger de la mort - Finale",
            "original": False,
            "question_ids": [str(q.id) for q in self.questions],
        }

    # 201 Created
    def test_create_deadly_burgers_success(self):
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["title"], self.valid_payload["title"])
        db = DeadlyBurger.objects.get(title=self.valid_payload["title"])
        self.assertEqual(db.questions.count(), 10)

    # 400 Bad Request
    def test_create_deadly_burgers_missing_title(self):
        payload = self.valid_payload.copy()
        payload.pop("title")
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_create_deadly_burgers_not_ten_questions(self):
        payload = {
            "title": "DB 9 questions",
            "original": False,
            "question_ids": [str(q.id) for q in self.questions[:9]],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_deadly_burgers_eleven_questions(self):
        q_extra = QuestionFactory.create_db("DB11")
        payload = {
            "title": "DB 11 questions",
            "original": False,
            "question_ids": [str(q.id) for q in self.questions] + [str(q_extra.id)],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_deadly_burgers_nonexistent_question_id(self):
        payload = {
            **self.valid_payload,
            "question_ids": [str(q.id) for q in self.questions[:9]] + [str(uuid.uuid4())],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

