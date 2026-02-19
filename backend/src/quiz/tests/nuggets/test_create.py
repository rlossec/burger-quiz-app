# python manage.py test quiz.tests.nuggets.test_create
# POST /api/quiz/nuggets/ — Nombre pair de questions, type NU, pas de doublon.

import uuid

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...models import Question, Nuggets
from ...tests.factories import QuestionFactory, NuggetsFactory


class TestNuggetsCreateEndpoint(APITestCase):
    """POST /api/quiz/nuggets/ — Nombre pair de questions, type NU, pas de doublon."""

    def setUp(self):
        self.url = reverse("nuggets-list")
        self.q1, self.q2, self.q3, self.q4 = (
            QuestionFactory.create_nu("N1"),
            QuestionFactory.create_nu("N2"),
            QuestionFactory.create_nu("N3"),
            QuestionFactory.create_nu("N4"),
        )
        self.valid_payload = {
            "title": "Culture générale",
            "original": False,
            "question_ids": [str(self.q1.id), str(self.q2.id), str(self.q3.id), str(self.q4.id)],
        }

    def test_create_success_returns_201(self):
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["title"], self.valid_payload["title"])
        self.assertEqual(response.data["original"], False)
        n = Nuggets.objects.get(title=self.valid_payload["title"])
        self.assertEqual(n.questions.count(), 4)

    def test_create_missing_title_returns_400(self):
        payload = self.valid_payload.copy()
        payload.pop("title")
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_create_odd_number_of_questions_returns_400(self):
        """Contrainte : nombre de questions pair (spéc §2.1, §6)."""
        payload = {
            "title": "Nuggets impair",
            "original": False,
            "question_ids": [str(self.q1.id), str(self.q2.id), str(self.q3.id)],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_question_wrong_type_returns_400(self):
        """Toutes les questions doivent être de type NU (spéc §2.1)."""
        q_sp = QuestionFactory.create_sp("Q SP")
        payload = {
            "title": "Nuggets mixte",
            "original": False,
            "question_ids": [str(self.q1.id), str(self.q2.id), str(q_sp.id), str(self.q4.id)],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_question_ids_returns_400(self):
        """Pas de doublon dans question_ids (spéc §2.1)."""
        payload = {
            "title": "Nuggets doublon",
            "original": False,
            "question_ids": [str(self.q1.id), str(self.q2.id), str(self.q1.id), str(self.q4.id)],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_nonexistent_question_id_returns_400(self):
        payload = {
            "title": "Nuggets fantôme",
            "original": False,
            "question_ids": [str(self.q1.id), str(self.q2.id), str(uuid.uuid4()), str(self.q4.id)],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
