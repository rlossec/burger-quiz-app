# python manage.py test quiz.tests.additions.test_create
# POST /api/quiz/additions/ — Questions type AD, pas de doublon.

import uuid

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...models import Addition
from ...tests.factories import QuestionFactory
from ...tests import MANDATORY_FIELD_ERROR_MESSAGE, DUPLICATE_QUESTION_IDS_ERROR_MESSAGE, NONE_EXISTENT_QUESTION_ID_ERROR_MESSAGE

User = get_user_model()


class TestAdditionCreateEndpoint(APITestCase):
    """POST /api/quiz/additions/ — Questions type AD, pas de doublon."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("addition-list")
        self.q1 = QuestionFactory.create_ad("AD1")
        self.q2 = QuestionFactory.create_ad("AD2")
        self.q3 = QuestionFactory.create_ad("AD3")
        self.valid_payload = {
            "title": "Addition rapide",
            "description": "Optionnel",
            "original": False,
            "questions": [str(self.q1.id), str(self.q2.id), str(self.q3.id)],
        }

    # 201 Created
    def test_create_additions_success(self):
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        # Check response data
        self.assertEqual(response.data["title"], self.valid_payload["title"])
        self.assertEqual(response.data["description"], self.valid_payload["description"])
        self.assertEqual(response.data["original"], self.valid_payload["original"])
        # Les questions sont désérialisées avec leur contenu complet
        questions = response.data["questions"]
        self.assertEqual(len(questions), 3)
        self.assertEqual(questions[0]["id"], str(self.q1.id))
        self.assertEqual(questions[0]["text"], self.q1.text)
        self.assertIn("answers", questions[0])
        # Check addition object
        a = Addition.objects.get(title=self.valid_payload["title"])
        self.assertEqual(a.questions.count(), 3)

    def test_create_additions_with_only_title_and_question_ids(self):
        payload = {
            "title": "Addition rapide",
            "question_ids": [str(self.q1.id), str(self.q2.id), str(self.q3.id)],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], payload["title"])
        # Les questions sont désérialisées avec leur contenu complet
        questions = response.data["questions"]
        self.assertEqual(len(questions), 3)
        self.assertEqual(questions[0]["id"], str(self.q1.id))
        self.assertEqual(response.data["description"], None)
        self.assertEqual(response.data["original"], True)

    # 400 Bad Request
    def test_create_additions_missing_title(self):
        payload = self.valid_payload.copy()
        payload.pop("title")
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)
        self.assertEqual(response.data["title"], [MANDATORY_FIELD_ERROR_MESSAGE])

    def test_create_additions_duplicate_question_ids(self):
        payload = {
            "title": self.valid_payload["title"],
            "question_ids": [str(self.q1.id), str(self.q2.id), str(self.q1.id)],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["question_ids"], [DUPLICATE_QUESTION_IDS_ERROR_MESSAGE])

    def test_create_additions_nonexistent_question_id(self):
        payload = {
            "title": self.valid_payload["title"],
            "question_ids": [str(self.q1.id), str(uuid.uuid4()), str(self.q3.id)],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["question_ids"], [NONE_EXISTENT_QUESTION_ID_ERROR_MESSAGE])
