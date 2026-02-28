# python manage.py test quiz.tests.interludes.test_update
# PUT/PATCH /api/quiz/interludes/{id}/ — Mise à jour d'un interlude vidéo.

import uuid

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..factories import VideoInterludeFactory
from .. import INTERLUDE_TYPE_IN, INTERLUDE_TYPE_PU

User = get_user_model()


class TestInterludeUpdateEndpoint(APITestCase):
    """PUT/PATCH /api/quiz/interludes/{id}/ — Mise à jour d'un interlude."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="test_user",
            email="test@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.interlude = VideoInterludeFactory.create_intro(
            title="Intro originale",
            youtube_url="https://www.youtube.com/watch?v=original",
            duration_seconds=30,
            skip_after_seconds=5,
            author=self.user,
        )
        self.url = reverse("interlude-detail", kwargs={"pk": self.interlude.pk})

    def test_patch_interlude_title(self):
        """PATCH pour modifier le titre."""
        response = self.client.patch(
            self.url,
            {"title": "Intro modifiée"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Intro modifiée")
        self.interlude.refresh_from_db()
        self.assertEqual(self.interlude.title, "Intro modifiée")

    def test_patch_interlude_skip_after_seconds(self):
        """PATCH pour modifier skip_after_seconds."""
        response = self.client.patch(
            self.url,
            {"skip_after_seconds": 10},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["skip_after_seconds"], 10)

    def test_patch_interlude_youtube_url(self):
        """PATCH pour modifier l'URL YouTube."""
        response = self.client.patch(
            self.url,
            {"youtube_url": "https://www.youtube.com/watch?v=newvideo"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["youtube_video_id"], "newvideo")

    def test_patch_interlude_type(self):
        """PATCH pour modifier le type d'interlude."""
        response = self.client.patch(
            self.url,
            {"interlude_type": INTERLUDE_TYPE_PU},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["interlude_type"], INTERLUDE_TYPE_PU)

    def test_put_interlude_full_update(self):
        """PUT pour mise à jour complète."""
        payload = {
            "title": "Nouvelle intro",
            "youtube_url": "https://www.youtube.com/watch?v=fullupdate",
            "interlude_type": INTERLUDE_TYPE_IN,
            "duration_seconds": 60,
            "autoplay": False,
            "skip_allowed": False,
            "skip_after_seconds": None,
        }
        response = self.client.put(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Nouvelle intro")
        self.assertEqual(response.data["youtube_video_id"], "fullupdate")
        self.assertEqual(response.data["duration_seconds"], 60)
        self.assertEqual(response.data["autoplay"], False)
        self.assertEqual(response.data["skip_allowed"], False)

    def test_patch_interlude_invalid_youtube_url(self):
        """PATCH avec URL YouTube invalide échoue."""
        response = self.client.patch(
            self.url,
            {"youtube_url": "https://example.com/invalid"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("youtube_url", response.data)

    def test_update_interlude_not_found(self):
        """404 si l'interlude n'existe pas."""
        url = reverse("interlude-detail", kwargs={"pk": uuid.uuid4()})
        response = self.client.patch(url, {"title": "Test"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_does_not_change_author(self):
        """PATCH ne modifie pas l'auteur."""
        other_user = User.objects.create_user(
            username="other_user",
            email="other@example.com",
            password="OtherPassword123!",
        )
        response = self.client.patch(
            self.url,
            {"title": "Titre modifié"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.interlude.refresh_from_db()
        self.assertEqual(self.interlude.author, self.user)
