import uuid

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...tests.factories import MenusFactory

User = get_user_model()


class TestMenusDetailEndpoint(APITestCase):
    """
    Test de l'endpoint GET /api/quiz/menus/{id}/
    Commande : uv run manage.py test quiz.tests.menus.test_detail
    """

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.menus = MenusFactory.create(title="Menus du jour", original=False)
        self.url = reverse("menus-detail", kwargs={"pk": self.menus.pk})

    # 200 OK
    def test_detail_menus_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), self.menus.title)
        self.assertIn("menu_1", response.data)
        self.assertIn("menu_2", response.data)
        self.assertIn("menu_troll", response.data)

    # 404 Not Found
    def test_detail_menus_not_found(self):
        url = reverse("menus-detail", kwargs={"pk": uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
