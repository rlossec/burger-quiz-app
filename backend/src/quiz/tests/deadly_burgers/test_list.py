# python manage.py test quiz.tests.deadly_burgers.test_list
# GET /api/quiz/deadly-burgers/ — Liste des manches Burger de la mort.

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class TestDeadlyBurgerListEndpoint(APITestCase):
    """GET /api/quiz/deadly-burgers/ — Liste des manches Burger de la mort."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("deadly-burger-list")

    # 200 OK
    def test_list_deadly_burgers_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
