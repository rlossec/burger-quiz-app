# python manage.py test quiz.tests.nuggets.test_update
# PATCH / PUT /api/quiz/nuggets/{id}/ — Mise à jour avec re-vérification des contraintes.

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...tests.factories import QuestionFactory, NuggetsFactory

User = get_user_model()

User = get_user_model()


class TestNuggetsUpdateEndpoint(APITestCase):
    """PATCH / PUT /api/quiz/nuggets/{id}/ — Mise à jour avec re-vérification des contraintes."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.q1 = QuestionFactory.create_nu("U1")
        self.q2 = QuestionFactory.create_nu("U2")
        self.nuggets = NuggetsFactory.create(
            title="Nuggets à modifier", original=False, questions=[self.q1, self.q2]
        )
        self.url = reverse("nuggets-detail", kwargs={"pk": self.nuggets.pk})

    def test_patch_title_returns_200(self):
        response = self.client.patch(
            self.url, {"title": "Nouveau titre"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Nouveau titre")

    def test_patch_original_returns_200(self):
        response = self.client.patch(self.url, {"original": True}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["original"], True)

    def test_put_odd_questions_returns_400(self):
        q3 = QuestionFactory.create_nu("U3")
        payload = {
            "title": self.nuggets.title,
            "original": self.nuggets.original,
            "question_ids": [str(self.q1.id), str(self.q2.id), str(q3.id)],
        }
        response = self.client.put(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
