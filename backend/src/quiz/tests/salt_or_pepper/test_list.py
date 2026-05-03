# uv run manage.py test quiz.tests.salt_or_pepper.test_list
# GET /api/quiz/salt-or-pepper/ — Liste des manches Sel ou poivre.

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..factories import SaltOrPepperFactory, QuestionFactory
from ..mixins import (
    AuthRequiredMixin,
    AuthorInListResponseMixin,
    TagsInListResponseMixin,
    TimestampsInListResponseMixin,
)

User = get_user_model()


class TestSaltOrPepperListEndpoint(APITestCase):
    """GET /api/quiz/salt-or-pepper/ — Liste des manches Sel ou poivre."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("salt-or-pepper-list")

    def test_list_salt_or_pepper_success(self):
        SaltOrPepperFactory.create()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_exposes_basic_fields(self):
        SaltOrPepperFactory.create(title="Noir ou Blanc", original=False)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data.get("results", response.data)
        self.assertTrue(len(data) > 0)
        item = data[0]
        self.assertIn("id", item)
        self.assertIn("title", item)
        self.assertIn("original", item)
        self.assertIn("propositions", item)

    def test_list_includes_questions_with_details(self):
        """La liste expose les questions complètes avec leurs réponses."""
        propositions = ["Noir", "Blanc", "Les deux"]
        questions = QuestionFactory.create_batch_sp(3, propositions=propositions)
        sop = SaltOrPepperFactory.create_with_questions(
            title="SP avec questions",
            propositions=propositions,
            questions=questions,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data.get("results", response.data)
        sop_data = next((s for s in data if str(s["id"]) == str(sop.id)), None)
        self.assertIsNotNone(sop_data)

        self.assertIn("questions", sop_data)
        self.assertEqual(len(sop_data["questions"]), 3)

        question = sop_data["questions"][0]
        self.assertIn("id", question)
        self.assertIn("text", question)
        self.assertIn("question_type", question)
        self.assertIn("answers", question)
        self.assertEqual(question["question_type"], "SP")

    def test_list_questions_include_answers(self):
        """Les questions dans la liste incluent leurs réponses."""
        propositions = ["Oui", "Non"]
        questions = QuestionFactory.create_batch_sp(2, propositions=propositions)
        SaltOrPepperFactory.create_with_questions(
            propositions=propositions,
            questions=questions,
        )
        response = self.client.get(self.url)

        data = response.data.get("results", response.data)
        self.assertTrue(len(data) > 0)

        question = data[0]["questions"][0]
        self.assertIn("answers", question)
        self.assertTrue(len(question["answers"]) > 0)

        answer = question["answers"][0]
        self.assertIn("text", answer)
        self.assertIn("is_correct", answer)

    def test_list_includes_propositions(self):
        """La liste expose les propositions de chaque manche."""
        propositions = ["Rouge", "Bleu", "Vert"]
        SaltOrPepperFactory.create(propositions=propositions)
        response = self.client.get(self.url)

        data = response.data.get("results", response.data)
        self.assertTrue(len(data) > 0)
        self.assertIn("propositions", data[0])
        self.assertEqual(data[0]["propositions"], propositions)


# ---------------------------------------------------------------------------
# Tests d'authentification requise (via mixin)
# ---------------------------------------------------------------------------


class TestSaltOrPepperAuthRequired(AuthRequiredMixin, APITestCase):
    """Tests d'authentification requise pour SaltOrPepper."""

    url_basename = "salt-or-pepper"


# ---------------------------------------------------------------------------
# Tests Author, Tags, Timestamps dans la liste (via mixins)
# ---------------------------------------------------------------------------


class TestSaltOrPepperListAuthor(AuthorInListResponseMixin, APITestCase):
    """Tests author dans la liste de SaltOrPepper."""

    factory = SaltOrPepperFactory
    url_basename = "salt-or-pepper"

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="author_list_user",
            email="author_list@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)


class TestSaltOrPepperListTags(TagsInListResponseMixin, APITestCase):
    """Tests tags dans la liste de SaltOrPepper."""

    factory = SaltOrPepperFactory
    url_basename = "salt-or-pepper"

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="tags_list_user",
            email="tags_list@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)


class TestSaltOrPepperListTimestamps(TimestampsInListResponseMixin, APITestCase):
    """Tests timestamps dans la liste de SaltOrPepper."""

    factory = SaltOrPepperFactory
    url_basename = "salt-or-pepper"

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="timestamps_list_user",
            email="timestamps_list@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
