# python manage.py test quiz.tests.interludes.test_detail
# GET /api/quiz/interludes/{id}/ — Détail d'un interlude vidéo.

import uuid

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..factories import VideoInterludeFactory, UserFactory

User = get_user_model()


class TestInterludeDetailEndpoint(APITestCase):
    """GET /api/quiz/interludes/{id}/ — Détail d'un interlude."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="test_user",
            email="test@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.author = UserFactory.create_author(username="author_user")
        self.interlude = VideoInterludeFactory.create_intro(
            title="Intro Burger Quiz",
            youtube_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            duration_seconds=45,
            autoplay=True,
            skip_allowed=True,
            skip_after_seconds=5,
            author=self.author,
        )
        self.url = reverse("interlude-detail", kwargs={"pk": self.interlude.pk})

    def test_detail_interlude_success(self):
        """Détail d'un interlude existant."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.interlude.id))
        self.assertEqual(response.data["title"], "Intro Burger Quiz")
        self.assertEqual(response.data["youtube_url"], "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        self.assertEqual(response.data["youtube_video_id"], "dQw4w9WgXcQ")
        self.assertEqual(response.data["interlude_type"], "IN")
        self.assertEqual(response.data["duration_seconds"], 45)
        self.assertEqual(response.data["autoplay"], True)
        self.assertEqual(response.data["skip_allowed"], True)
        self.assertEqual(response.data["skip_after_seconds"], 5)

    def test_detail_interlude_includes_author(self):
        """Le détail inclut l'auteur."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("author", response.data)
        self.assertEqual(response.data["author"]["id"], self.author.id)
        self.assertEqual(response.data["author"]["username"], "author_user")

    def test_detail_interlude_includes_timestamps(self):
        """Le détail inclut created_at et updated_at."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)

    def test_detail_interlude_not_found(self):
        """404 si l'interlude n'existe pas."""
        url = reverse("interlude-detail", kwargs={"pk": uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
