# python manage.py test quiz.tests.additions.test_list
# GET /api/quiz/additions/ — Liste des manches Addition.

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class TestAdditionListEndpoint(APITestCase):
    """GET /api/quiz/additions/ — Liste des manches Addition."""

    def setUp(self):
        self.url = reverse("addition-list")

    # 200 OK
    def test_list_additions_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
