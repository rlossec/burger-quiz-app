# python manage.py test quiz.tests.burger_quizzes.test_detail
# GET /api/quiz/burger-quizzes/{id}/ — Détail.

import uuid

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...tests.factories import (
    BurgerQuizFactory,
    VideoInterludeFactory,
    BurgerQuizElementFactory,
)
from .. import QUESTION_TYPE_NU, QUESTION_TYPE_SP

User = get_user_model()


class TestBurgerQuizDetailEndpoint(APITestCase):
    """GET /api/quiz/burger-quizzes/{id}/ — Détail."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
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

    def test_detail_includes_structure(self):
        """Le détail inclut la structure du quiz."""
        bq = BurgerQuizFactory.create_full(title="Quiz avec structure")
        intro = VideoInterludeFactory.create_intro(title="Intro")
        
        BurgerQuizElementFactory.create_interlude(bq, order=1, interlude=intro)
        BurgerQuizElementFactory.create_round(bq, order=2, round_type=QUESTION_TYPE_NU)
        BurgerQuizElementFactory.create_round(bq, order=3, round_type=QUESTION_TYPE_SP)
        
        url = reverse("burger-quiz-detail", kwargs={"pk": bq.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("structure", response.data)
        self.assertEqual(len(response.data["structure"]), 3)
        
        self.assertEqual(response.data["structure"][0]["element_type"], "interlude")
        self.assertIn("interlude", response.data["structure"][0])
        self.assertEqual(response.data["structure"][0]["interlude"]["title"], "Intro")
        
        self.assertEqual(response.data["structure"][1]["element_type"], "round")
        self.assertEqual(response.data["structure"][1]["round_type"], QUESTION_TYPE_NU)

    def test_detail_structure_empty_if_not_configured(self):
        """La structure est vide ou par défaut si non configurée."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("structure", response.data)
