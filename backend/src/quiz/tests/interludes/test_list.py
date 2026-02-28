# python manage.py test quiz.tests.interludes.test_list
# GET /api/quiz/interludes/ — Liste des interludes vidéo.

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..factories import VideoInterludeFactory
from .. import (
    INTERLUDE_TYPE_IN,
    INTERLUDE_TYPE_OU,
    INTERLUDE_TYPE_PU,
)

User = get_user_model()


class TestInterludeListEndpoint(APITestCase):
    """GET /api/quiz/interludes/ — Liste des interludes."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="test_user",
            email="test@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("interlude-list")

    def test_list_interludes_empty(self):
        """Liste vide si aucun interlude."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(response.data["results"], [])

    def test_list_interludes_with_data(self):
        """Liste avec interludes existants."""
        VideoInterludeFactory.create_intro(title="Intro 1")
        VideoInterludeFactory.create_pub(title="Pub 1")
        VideoInterludeFactory.create_outro(title="Outro 1")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)
        self.assertEqual(len(response.data["results"]), 3)

    def test_list_interludes_filter_by_type_intro(self):
        """Filtre par type d'interlude (intro)."""
        VideoInterludeFactory.create_intro(title="Intro 1")
        VideoInterludeFactory.create_pub(title="Pub 1")

        response = self.client.get(self.url, {"interlude_type": INTERLUDE_TYPE_IN})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["interlude_type"], INTERLUDE_TYPE_IN)

    def test_list_interludes_filter_by_type_pub(self):
        """Filtre par type d'interlude (pub)."""
        VideoInterludeFactory.create_intro(title="Intro 1")
        VideoInterludeFactory.create_pub(title="Pub 1")
        VideoInterludeFactory.create_pub(title="Pub 2")

        response = self.client.get(self.url, {"interlude_type": INTERLUDE_TYPE_PU})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_list_interludes_search_by_title(self):
        """Recherche textuelle sur le titre."""
        VideoInterludeFactory.create_intro(title="Intro Burger Quiz")
        VideoInterludeFactory.create_pub(title="Pub Ketchup")
        VideoInterludeFactory.create_pub(title="Pub Moutarde")

        response = self.client.get(self.url, {"search": "Ketchup"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], "Pub Ketchup")

    def test_list_interludes_combined_filters(self):
        """Combinaison de filtres (type + search)."""
        VideoInterludeFactory.create_pub(title="Pub Ketchup")
        VideoInterludeFactory.create_pub(title="Pub Moutarde")
        VideoInterludeFactory.create_intro(title="Intro Ketchup")

        response = self.client.get(
            self.url,
            {"interlude_type": INTERLUDE_TYPE_PU, "search": "Ketchup"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], "Pub Ketchup")

    def test_list_interludes_response_fields(self):
        """Vérifie les champs retournés dans la liste."""
        VideoInterludeFactory.create_intro(
            title="Intro Test",
            youtube_url="https://www.youtube.com/watch?v=abc123",
            duration_seconds=45,
            autoplay=True,
            skip_allowed=True,
            skip_after_seconds=5,
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        item = response.data["results"][0]
        self.assertIn("id", item)
        self.assertIn("title", item)
        self.assertIn("youtube_url", item)
        self.assertIn("youtube_video_id", item)
        self.assertIn("interlude_type", item)
        self.assertIn("duration_seconds", item)
        self.assertIn("autoplay", item)
        self.assertIn("skip_allowed", item)
        self.assertIn("skip_after_seconds", item)
        self.assertIn("created_at", item)
        self.assertIn("updated_at", item)
