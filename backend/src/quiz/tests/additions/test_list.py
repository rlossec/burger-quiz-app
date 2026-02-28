# python manage.py test quiz.tests.additions.test_list
# GET /api/quiz/additions/ — Liste des manches Addition.

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..factories import AdditionFactory, QuestionFactory
from ..mixins import (
    AuthRequiredMixin,
    AuthorInListResponseMixin,
    TagsInListResponseMixin,
    TimestampsInListResponseMixin,
)

User = get_user_model()


class TestAdditionListEndpoint(APITestCase):
    """GET /api/quiz/additions/ — Liste des manches Addition."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("addition-list")

    def test_list_additions_success(self):
        AdditionFactory.create()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_exposes_basic_fields(self):
        AdditionFactory.create(title="Addition rapide", original=False)
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
        questions = QuestionFactory.create_batch_ad(3)
        addition = AdditionFactory.create(
            title="Addition avec questions",
            questions=questions,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data.get("results", response.data)
        addition_data = next((a for a in data if str(a["id"]) == str(addition.id)), None)
        self.assertIsNotNone(addition_data)

        self.assertIn("questions", addition_data)
        self.assertEqual(len(addition_data["questions"]), 3)

        question = addition_data["questions"][0]
        self.assertIn("id", question)
        self.assertIn("text", question)
        self.assertIn("question_type", question)
        self.assertIn("answers", question)
        self.assertEqual(question["question_type"], "AD")

    def test_list_questions_include_answers(self):
        """Les questions dans la liste incluent leurs réponses."""
        questions = QuestionFactory.create_batch_ad(2)
        AdditionFactory.create(questions=questions)
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


class TestAdditionAuthRequired(AuthRequiredMixin, APITestCase):
    """Tests d'authentification requise pour Addition."""

    url_basename = "addition"


# ---------------------------------------------------------------------------
# Tests Author, Tags, Timestamps dans la liste (via mixins)
# ---------------------------------------------------------------------------


class TestAdditionListAuthor(AuthorInListResponseMixin, APITestCase):
    """Tests author dans la liste d'Addition."""

    factory = AdditionFactory
    url_basename = "addition"

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="author_list_user",
            email="author_list@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)


class TestAdditionListTags(TagsInListResponseMixin, APITestCase):
    """Tests tags dans la liste d'Addition."""

    factory = AdditionFactory
    url_basename = "addition"

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="tags_list_user",
            email="tags_list@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)


class TestAdditionListTimestamps(TimestampsInListResponseMixin, APITestCase):
    """Tests timestamps dans la liste d'Addition."""

    factory = AdditionFactory
    url_basename = "addition"

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="timestamps_list_user",
            email="timestamps_list@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
