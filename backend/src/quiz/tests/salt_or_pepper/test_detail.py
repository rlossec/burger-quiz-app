# uv run manage.py test quiz.tests.salt_or_pepper.test_detail
# GET /api/quiz/salt-or-pepper/{id}/ — Détail.

import uuid

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..factories import SaltOrPepperFactory
from ..mixins import (
    AuthorInDetailResponseMixin,
    TagsInDetailResponseMixin,
    TimestampsInDetailResponseMixin,
)

User = get_user_model()


class TestSaltOrPepperDetailEndpoint(APITestCase):
    """GET /api/quiz/salt-or-pepper/{id}/ — Détail."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.sop = SaltOrPepperFactory.create(
            title="Noir ou Blanc",
            choice_labels=["Noir", "Blanc"],
            original=False,
        )
        self.url = reverse("salt-or-pepper-detail", kwargs={"pk": self.sop.pk})

    # 200 OK
    def test_detail_salt_or_pepper_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), self.sop.title)
        self.assertIn("propositions", response.data)
        self.assertEqual(response.data["propositions"], ["Noir", "Blanc"])

    # 404 Not Found
    def test_detail_salt_or_pepper_not_found(self):
        url = reverse("salt-or-pepper-detail", kwargs={"pk": uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# ---------------------------------------------------------------------------
# Tests Author, Tags, Timestamps dans le détail (via mixins)
# ---------------------------------------------------------------------------


class TestSaltOrPepperDetailAuthor(AuthorInDetailResponseMixin, APITestCase):
    """Tests author dans le détail de SaltOrPepper."""

    factory = SaltOrPepperFactory
    url_basename = "salt-or-pepper"

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="author_detail_user",
            email="author_detail@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)


class TestSaltOrPepperDetailTags(TagsInDetailResponseMixin, APITestCase):
    """Tests tags dans le détail de SaltOrPepper."""

    factory = SaltOrPepperFactory
    url_basename = "salt-or-pepper"

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="tags_detail_user",
            email="tags_detail@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)


class TestSaltOrPepperDetailTimestamps(TimestampsInDetailResponseMixin, APITestCase):
    """Tests timestamps dans le détail de SaltOrPepper."""

    factory = SaltOrPepperFactory
    url_basename = "salt-or-pepper"

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="timestamps_detail_user",
            email="timestamps_detail@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
