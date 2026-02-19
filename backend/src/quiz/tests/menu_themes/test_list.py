# python manage.py test quiz.tests.menu_themes.test_list
# GET /api/quiz/menu-themes/ — Liste des thèmes de menu.

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class TestMenuThemeListEndpoint(APITestCase):
    """GET /api/quiz/menu-themes/ — Liste des thèmes de menu."""

    def setUp(self):
        self.url = reverse("menu-theme-list")

    # 200 OK
    def test_list_menu_themes_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
