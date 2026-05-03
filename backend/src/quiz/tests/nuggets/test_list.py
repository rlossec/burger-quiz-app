# python manage.py test quiz.tests.nuggets.test_list
# GET /api/quiz/nuggets/ — Liste des manches Nuggets.

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..factories import NuggetsFactory, QuestionFactory
from ..mixins import (
    AuthRequiredMixin,
    AuthorInListResponseMixin,
    TagsInListResponseMixin,
    TimestampsInListResponseMixin,
)

User = get_user_model()


class TestNuggetsListEndpoint(APITestCase):
    """GET /api/quiz/nuggets/ — Liste des manches Nuggets."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("nuggets-list")

    def test_list_returns_200(self):
        NuggetsFactory.create(title="Culture générale", original=False)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_exposes_basic_fields(self):
        NuggetsFactory.create(title="Culture générale", original=False)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data.get("results", response.data)
        self.assertTrue(len(data) > 0)
        item = data[0]
        self.assertIn("id", item)
        self.assertIn("title", item)
        self.assertIn("original", item)

    def test_list_includes_questions_with_details(self):
        """La liste expose les questions complètes avec leurs réponses."""
        questions = QuestionFactory.create_batch_nu(4)
        nuggets = NuggetsFactory.create_with_questions(
            title="Nuggets avec questions",
            questions=questions,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data.get("results", response.data)
        nuggets_data = next((n for n in data if str(n["id"]) == str(nuggets.id)), None)
        self.assertIsNotNone(nuggets_data)

        self.assertIn("questions", nuggets_data)
        self.assertEqual(len(nuggets_data["questions"]), 4)

        question = nuggets_data["questions"][0]
        self.assertIn("id", question)
        self.assertIn("text", question)
        self.assertIn("question_type", question)
        self.assertIn("answers", question)
        self.assertEqual(question["question_type"], "NU")

    def test_list_questions_include_answers(self):
        """Les questions dans la liste incluent leurs réponses."""
        questions = QuestionFactory.create_batch_nu(2)
        NuggetsFactory.create_with_questions(questions=questions)
        response = self.client.get(self.url)

        data = response.data.get("results", response.data)
        self.assertTrue(len(data) > 0)

        question = data[0]["questions"][0]
        self.assertIn("answers", question)
        self.assertTrue(len(question["answers"]) > 0)

        answer = question["answers"][0]
        self.assertIn("text", answer)
        self.assertIn("is_correct", answer)


# ---------------------------------------------------------------------------
# Tests d'authentification requise (via mixin)
# ---------------------------------------------------------------------------


class TestNuggetsAuthRequired(AuthRequiredMixin, APITestCase):
    """Tests d'authentification requise pour Nuggets."""

    url_basename = "nuggets"


# ---------------------------------------------------------------------------
# Tests Author, Tags, Timestamps dans la liste (via mixins)
# ---------------------------------------------------------------------------


class TestNuggetsListAuthor(AuthorInListResponseMixin, APITestCase):
    """Tests author dans la liste de Nuggets."""

    factory = NuggetsFactory
    url_basename = "nuggets"

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="author_list_user",
            email="author_list@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)


class TestNuggetsListTags(TagsInListResponseMixin, APITestCase):
    """Tests tags dans la liste de Nuggets."""

    factory = NuggetsFactory
    url_basename = "nuggets"

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="tags_list_user",
            email="tags_list@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)


class TestNuggetsListTimestamps(TimestampsInListResponseMixin, APITestCase):
    """Tests timestamps dans la liste de Nuggets."""

    factory = NuggetsFactory
    url_basename = "nuggets"

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="timestamps_list_user",
            email="timestamps_list@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
