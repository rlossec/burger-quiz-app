# python manage.py test quiz.tests.deadly_burgers.test_list
# GET /api/quiz/deadly-burgers/ — Liste des manches Burger de la mort.

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..factories import DeadlyBurgerFactory, QuestionFactory
from ..mixins import (
    AuthRequiredMixin,
    AuthorInListResponseMixin,
    TagsInListResponseMixin,
    TimestampsInListResponseMixin,
)

User = get_user_model()


class TestDeadlyBurgerListEndpoint(APITestCase):
    """GET /api/quiz/deadly-burgers/ — Liste des manches Burger de la mort."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("deadly-burger-list")

    def test_list_deadly_burgers_success(self):
        DeadlyBurgerFactory.create()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_exposes_basic_fields(self):
        DeadlyBurgerFactory.create(title="Burger de la mort - Finale", original=False)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data.get("results", response.data)
        self.assertTrue(len(data) > 0)
        item = data[0]
        self.assertIn("id", item)
        self.assertIn("title", item)
        self.assertIn("original", item)

    def test_list_includes_questions_with_details(self):
        """La liste expose les questions complètes."""
        questions = QuestionFactory.create_batch_db(10)
        db = DeadlyBurgerFactory.create(
            title="DB avec questions",
            questions=questions,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data.get("results", response.data)
        db_data = next((d for d in data if str(d["id"]) == str(db.id)), None)
        self.assertIsNotNone(db_data)

        self.assertIn("questions", db_data)
        self.assertEqual(len(db_data["questions"]), 10)

        question = db_data["questions"][0]
        self.assertIn("id", question)
        self.assertIn("text", question)
        self.assertIn("question_type", question)
        self.assertEqual(question["question_type"], "DB")

    def test_list_questions_are_present(self):
        """Les questions DB sont présentes dans la liste."""
        questions = QuestionFactory.create_batch_db(5)
        DeadlyBurgerFactory.create(questions=questions)
        response = self.client.get(self.url)

        data = response.data.get("results", response.data)
        self.assertTrue(len(data) > 0)
        self.assertIn("questions", data[0])
        self.assertEqual(len(data[0]["questions"]), 5)


# ---------------------------------------------------------------------------
# Tests d'authentification requise (via mixin)
# ---------------------------------------------------------------------------


class TestDeadlyBurgerAuthRequired(AuthRequiredMixin, APITestCase):
    """Tests d'authentification requise pour DeadlyBurger."""

    url_basename = "deadly-burger"


# ---------------------------------------------------------------------------
# Tests Author, Tags, Timestamps dans la liste (via mixins)
# ---------------------------------------------------------------------------


class TestDeadlyBurgerListAuthor(AuthorInListResponseMixin, APITestCase):
    """Tests author dans la liste de DeadlyBurger."""

    factory = DeadlyBurgerFactory
    url_basename = "deadly-burger"

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="author_list_user",
            email="author_list@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)


class TestDeadlyBurgerListTags(TagsInListResponseMixin, APITestCase):
    """Tests tags dans la liste de DeadlyBurger."""

    factory = DeadlyBurgerFactory
    url_basename = "deadly-burger"

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="tags_list_user",
            email="tags_list@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)


class TestDeadlyBurgerListTimestamps(TimestampsInListResponseMixin, APITestCase):
    """Tests timestamps dans la liste de DeadlyBurger."""

    factory = DeadlyBurgerFactory
    url_basename = "deadly-burger"

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="timestamps_list_user",
            email="timestamps_list@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
