# uv run manage.py test quiz.tests.salt_or_pepper.test_create
# POST /api/quiz/salt-or-pepper/ — 2 à 5 propositions, questions type SP, cohérence réponses.

import uuid

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...tests.factories import QuestionFactory

User = get_user_model()


class TestSaltOrPepperCreateEndpoint(APITestCase):
    """POST /api/quiz/salt-or-pepper/ — 2 à 5 propositions, questions type SP."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("salt-or-pepper-list")
        self.q1 = QuestionFactory.create_sp("SP1")
        self.q2 = QuestionFactory.create_sp("SP2")
        self.valid_payload = {
            "title": "Noir, Blanc ou Les deux",
            "original": False,
            "description": "Optionnel",
            "propositions": ["Noir", "Blanc", "Les deux"],
            "question_ids": [str(self.q1.id), str(self.q2.id)],
        }

    # 201 Created
    def test_create_salt_or_pepper_success(self):
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["title"], self.valid_payload["title"])
        self.assertEqual(
            len(response.data.get("propositions", response.data.get("choice_labels", []))), 3
        )

    # 400 Bad Request
    def test_create_salt_or_pepper_missing_title(self):
        payload = self.valid_payload.copy()
        payload.pop("title")
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_create_salt_or_pepper_missing_propositions(self):
        payload = self.valid_payload.copy()
        payload.pop("propositions")
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("propositions", response.data)

    def test_create_salt_or_pepper_propositions_too_few(self):
        payload = {**self.valid_payload, "propositions": ["Seul"]}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_salt_or_pepper_propositions_too_many(self):
        payload = {
            **self.valid_payload,
            "propositions": ["A", "B", "C", "D", "E", "F"],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_salt_or_pepper_propositions_duplicate(self):
        payload = {**self.valid_payload, "propositions": ["Noir", "Noir", "Blanc"]}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_salt_or_pepper_nonexistent_question_id(self):
        payload = {
            **self.valid_payload,
            "question_ids": [str(self.q1.id), str(uuid.uuid4())],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

