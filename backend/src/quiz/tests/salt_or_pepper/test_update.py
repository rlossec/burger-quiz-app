# uv run manage.py test quiz.tests.salt_or_pepper.test_update
# PATCH / PUT /api/quiz/salt-or-pepper/{id}/.

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..factories import SaltOrPepperFactory, QuestionFactory
from ..mixins import (
    AuthorNotChangedOnUpdateMixin,
    TagsUpdateMixin,
)

User = get_user_model()


class TestSaltOrPepperUpdateEndpoint(APITestCase):
    """PATCH / PUT /api/quiz/salt-or-pepper/{id}/."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.sop = SaltOrPepperFactory.create(
            title="SOP à modifier",
            choice_labels=["Oui", "Non"],
            original=False,
        )
        self.url = reverse("salt-or-pepper-detail", kwargs={"pk": self.sop.pk})

    # 200 OK
    def test_patch_salt_or_pepper_title_success(self):
        response = self.client.patch(
            self.url, {"title": "Nouveau titre SOP"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Nouveau titre SOP")


# ---------------------------------------------------------------------------
# Tests Author, Tags à la mise à jour (via mixins)
# ---------------------------------------------------------------------------


class TestSaltOrPepperUpdateAuthor(AuthorNotChangedOnUpdateMixin, APITestCase):
    """Tests author à la mise à jour de SaltOrPepper."""

    factory = SaltOrPepperFactory
    url_basename = "salt-or-pepper"

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="author_update_user",
            email="author_update@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.q1 = QuestionFactory.create_sp("SP1")

    def get_valid_payload(self):
        return {
            "title": "SOP Updated",
            "propositions": ["A", "B"],
            "question_ids": [str(self.q1.id)],
        }


class TestSaltOrPepperUpdateTags(TagsUpdateMixin, APITestCase):
    """Tests tags à la mise à jour de SaltOrPepper."""

    factory = SaltOrPepperFactory
    url_basename = "salt-or-pepper"

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="tags_update_user",
            email="tags_update@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.q1 = QuestionFactory.create_sp("SP1")

    def get_valid_payload(self):
        return {
            "title": "SOP Tags Updated",
            "propositions": ["A", "B"],
            "question_ids": [str(self.q1.id)],
        }
