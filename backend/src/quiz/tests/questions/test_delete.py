# python manage.py test quiz.tests.questions.test_delete
# DELETE /api/quiz/questions/<id>/ — Suppression (404 si id inconnu, cascade sur les réponses).

import uuid

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...models import Answer, Question
from ...tests.factories import QuestionFactory

User = get_user_model()


class TestQuestionDeleteEndpoint(APITestCase):
    """
    Test de l'endpoint DELETE /api/quiz/questions/<id>/
    Commande : uv run manage.py test quiz.tests.questions.test_delete
    """

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)

    def test_delete_unknown_id_returns_404(self):
        """Un id inexistant doit renvoyer 404."""
        fake_id = uuid.uuid4()
        url = reverse("question-detail", kwargs={"pk": fake_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_question_removes_answers_in_cascade(self):
        """La suppression d'une question doit supprimer ses réponses en cascade."""
        question = QuestionFactory.create_nu_with_answers(text="Question à supprimer")
        answer_ids = list(question.answers.values_list("id", flat=True))
        self.assertGreater(len(answer_ids), 0, "La question doit avoir des réponses")

        url = reverse("question-detail", kwargs={"pk": question.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(
            Question.objects.filter(pk=question.pk).exists(),
            "La question doit être supprimée",
        )
        self.assertEqual(
            Answer.objects.filter(pk__in=answer_ids).count(),
            0,
            "Les réponses doivent être supprimées en cascade",
        )
