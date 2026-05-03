# python manage.py test quiz.tests.menu_themes.test_detail
# GET /api/quiz/menu-themes/{id}/ — Détail.

import uuid

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...tests.factories import MenuThemeFactory

User = get_user_model()


class TestMenuThemeDetailEndpoint(APITestCase):
    """GET /api/quiz/menu-themes/{id}/ — Détail."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.theme = MenuThemeFactory.create_classic(title="Histoire de la gastronomie")
        self.url = reverse("menu-theme-detail", kwargs={"pk": self.theme.pk})

    # 200 OK
    def test_detail_menu_theme_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), self.theme.title)
        self.assertEqual(response.data.get("type"), self.theme.type)

    # 404 Not Found
    def test_detail_menu_theme_not_found(self):
        url = reverse("menu-theme-detail", kwargs={"pk": uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
