# python manage.py test quiz.tests.menus.test_list
# GET /api/quiz/menus/ — Liste des manches Menus.

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class TestMenusListEndpoint(APITestCase):
    """GET /api/quiz/menus/ — Liste des manches Menus."""

    def setUp(self):
        self.url = reverse("menus-list")

    # 200 OK
    def test_list_menus_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
