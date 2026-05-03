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
    NuggetsFactory,
    SaltOrPepperFactory,
    BurgerQuizElementFactory,
)

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

    def test_detail_includes_structure_light_by_default(self):
        """Sans expand : structure = order, type, id (léger)."""
        bq = BurgerQuizFactory.create(title="Quiz avec structure", toss="Toss")
        intro = VideoInterludeFactory.create_intro(title="Intro")

        BurgerQuizElementFactory.create_interlude(bq, order=1, interlude=intro)
        BurgerQuizElementFactory.create_round(bq, order=2, round_obj=NuggetsFactory.create())
        BurgerQuizElementFactory.create_round(bq, order=3, round_obj=SaltOrPepperFactory.create())

        url = reverse("burger-quiz-detail", kwargs={"pk": bq.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("structure", response.data)
        self.assertEqual(len(response.data["structure"]), 3)

        self.assertEqual(response.data["structure"][0]["type"], "video_interlude")
        self.assertNotIn("video_interlude", response.data["structure"][0])

        self.assertEqual(response.data["structure"][1]["type"], "nuggets")
        self.assertEqual(response.data["structure"][1]["order"], 2)

    def test_detail_structure_expand_full(self):
        """?expand=full : détail des manches dans la structure."""
        bq = BurgerQuizFactory.create(title="Quiz avec structure", toss="Toss")
        intro = VideoInterludeFactory.create_intro(title="Intro")

        BurgerQuizElementFactory.create_interlude(bq, order=1, interlude=intro)
        BurgerQuizElementFactory.create_round(bq, order=2, round_obj=NuggetsFactory.create())
        BurgerQuizElementFactory.create_round(bq, order=3, round_obj=SaltOrPepperFactory.create())

        url = reverse("burger-quiz-detail", kwargs={"pk": bq.pk})
        response = self.client.get(url, {"expand": "full"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["structure"][0]["type"], "video_interlude")
        self.assertIn("video_interlude", response.data["structure"][0])
        self.assertEqual(response.data["structure"][0]["video_interlude"]["title"], "Intro")

    def test_detail_structure_empty_if_not_configured(self):
        """Sans BurgerQuizElement : structure vide."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("structure", response.data)
        self.assertEqual(response.data["structure"], [])
