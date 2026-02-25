# python manage.py test quiz.tests.menus.test_list
# GET /api/quiz/menus/ — Liste des manches Menus.

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class TestMenusListEndpoint(APITestCase):
    """GET /api/quiz/menus/ — Liste des manches Menus."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("menus-list")

    # 200 OK
    def test_list_menus_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
