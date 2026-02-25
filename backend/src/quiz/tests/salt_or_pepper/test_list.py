# python manage.py test quiz.tests.salt_or_pepper.test_list
# GET /api/quiz/salt-or-pepper/ — Liste des manches Sel ou poivre.

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class TestSaltOrPepperListEndpoint(APITestCase):
    """GET /api/quiz/salt-or-pepper/ — Liste des manches Sel ou poivre."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("salt-or-pepper-list")

    def test_list_salt_or_pepper_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
