from unittest import skip
import uuid

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...tests.factories import QuestionFactory

User = get_user_model()


class TestQuestionDetailEndpoint(APITestCase):
    """
    Test de l'endpoint GET /api/quiz/questions/{id}/
    Commande : uv run manage.py test quiz.tests.questions.test_detail
    """

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.question = QuestionFactory.create_nu("Détail question")
        self.url = reverse("question-detail", kwargs={"pk": self.question.pk})

    # 200 OK
    def test_detail_question_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), str(self.question.id))
        self.assertEqual(response.data.get("text"), self.question.text)
        self.assertEqual(response.data.get("question_type"), self.question.question_type)
        self.assertEqual(response.data.get("original"), self.question.original)
    
    # 404 Not Found
    def test_detail_question_not_found(self):
        fake_id = uuid.uuid4()
        url = reverse("question-detail", kwargs={"pk": fake_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # 200 OK avec champ usage_count
    @skip("Not implemented")
    def test_detail_question_success_with_usage_count(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("usage_count"), self.question.usage_count)
