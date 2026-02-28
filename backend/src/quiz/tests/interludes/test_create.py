# python manage.py test quiz.tests.interludes.test_create
# POST /api/quiz/interludes/ — Création d'un interlude vidéo.

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...models import VideoInterlude
from .. import (
    MANDATORY_FIELD_ERROR_MESSAGE,
    INTERLUDE_TYPE_IN,
    INTERLUDE_TYPE_PU,
    INTERLUDE_INVALID_YOUTUBE_URL,
)

User = get_user_model()


class TestInterludeCreateEndpoint(APITestCase):
    """POST /api/quiz/interludes/ — Création d'un interlude."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="test_user",
            email="test@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("interlude-list")
        self.valid_payload = {
            "title": "Intro Burger Quiz",
            "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "interlude_type": INTERLUDE_TYPE_IN,
            "duration_seconds": 45,
            "autoplay": True,
            "skip_allowed": True,
            "skip_after_seconds": 5,
        }

    def test_create_interlude_success(self):
        """Création réussie avec tous les champs."""
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["title"], "Intro Burger Quiz")
        self.assertEqual(response.data["youtube_url"], "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        self.assertEqual(response.data["youtube_video_id"], "dQw4w9WgXcQ")
        self.assertEqual(response.data["interlude_type"], INTERLUDE_TYPE_IN)
        self.assertEqual(response.data["duration_seconds"], 45)
        
        interlude = VideoInterlude.objects.get(title="Intro Burger Quiz")
        self.assertEqual(interlude.youtube_video_id, "dQw4w9WgXcQ")

    def test_create_interlude_minimal_payload(self):
        """Création avec payload minimal (champs optionnels omis)."""
        payload = {
            "title": "Pub simple",
            "youtube_url": "https://www.youtube.com/watch?v=abc123",
            "interlude_type": INTERLUDE_TYPE_PU,
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["autoplay"], True)
        self.assertEqual(response.data["skip_allowed"], True)
        self.assertIsNone(response.data["skip_after_seconds"])

    def test_create_interlude_missing_title(self):
        """Erreur si titre manquant."""
        payload = self.valid_payload.copy()
        payload.pop("title")
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_create_interlude_missing_youtube_url(self):
        """Erreur si URL YouTube manquante."""
        payload = self.valid_payload.copy()
        payload.pop("youtube_url")
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("youtube_url", response.data)

    def test_create_interlude_default_interlude_type(self):
        """Le type d'interlude a une valeur par défaut (IL) si non fourni."""
        payload = self.valid_payload.copy()
        payload.pop("interlude_type")
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["interlude_type"], "IL")

    def test_create_interlude_invalid_youtube_url(self):
        """Erreur si URL YouTube invalide."""
        payload = self.valid_payload.copy()
        payload["youtube_url"] = "https://example.com/not-youtube"
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("youtube_url", response.data)

    def test_create_interlude_invalid_interlude_type(self):
        """Erreur si type d'interlude invalide."""
        payload = self.valid_payload.copy()
        payload["interlude_type"] = "XX"
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("interlude_type", response.data)

    def test_create_interlude_youtube_url_formats(self):
        """Différents formats d'URL YouTube sont acceptés."""
        youtube_urls = [
            ("https://www.youtube.com/watch?v=abc123", "abc123"),
            ("https://youtube.com/watch?v=def456", "def456"),
            ("https://youtu.be/ghi789", "ghi789"),
            ("https://www.youtube.com/embed/jkl012", "jkl012"),
        ]
        
        for url, expected_id in youtube_urls:
            payload = {
                "title": f"Test {expected_id}",
                "youtube_url": url,
                "interlude_type": INTERLUDE_TYPE_IN,
            }
            response = self.client.post(self.url, payload, format="json")
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                f"URL {url} should be valid",
            )
            self.assertEqual(
                response.data["youtube_video_id"],
                expected_id,
                f"Video ID for {url} should be {expected_id}",
            )

    def test_create_interlude_author_auto_assigned(self):
        """L'auteur est automatiquement assigné à l'utilisateur connecté."""
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        interlude = VideoInterlude.objects.get(id=response.data["id"])
        self.assertEqual(interlude.author, self.user)

    def test_create_interlude_with_tags(self):
        """Création avec tags."""
        from taggit.models import Tag
        Tag.objects.create(name="intro")
        Tag.objects.create(name="officiel")
        
        payload = {**self.valid_payload, "tags": ["intro", "officiel"]}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        interlude = VideoInterlude.objects.get(id=response.data["id"])
        self.assertEqual(interlude.tags.count(), 2)
