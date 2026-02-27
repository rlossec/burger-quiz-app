# uv run manage.py test quiz.tests.salt_or_pepper.test_list
# GET /api/quiz/salt-or-pepper/ — Liste des manches Sel ou poivre.

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..factories import SaltOrPepperFactory
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
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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
