# python manage.py test quiz.tests.tags.test_list
# GET /api/quiz/tags/ — autocomplétion des noms de tags (taggit).

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from taggit.models import Tag

User = get_user_model()


class TestTagListEndpoint(APITestCase):
    """GET /api/quiz/tags/ — liste filtrée pour autocomplétion."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="tags_list_user",
            email="tags_list@example.com",
            password="TagsListPassword123!",
        )
        self.url = reverse("quiz-tags")
        Tag.objects.create(name="culture", slug="culture")
        Tag.objects.create(name="cinema-scope", slug="cinema-scope")

    def test_tags_requires_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tags_returns_results_ordered_by_name(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], ["cinema-scope", "culture"])

    def test_tags_filters_by_q_icontains(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"q": "cult"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], ["culture"])

    def test_tags_respects_limit(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"limit": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0], "cinema-scope")
