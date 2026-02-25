# python manage.py test quiz.tests.menus.test_update
# PATCH / PUT /api/quiz/menus/{id}/.

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...tests.factories import MenusFactory

User = get_user_model()


class TestMenusUpdateEndpoint(APITestCase):
    """PATCH / PUT /api/quiz/menus/{id}/."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.menus = MenusFactory.create(title="Menus à modifier", original=False)
        self.url = reverse("menus-detail", kwargs={"pk": self.menus.pk})

    # 200 OK
    def test_patch_menus_title_success(self):
        response = self.client.patch(
            self.url, {"title": "Nouveau titre Menus"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Nouveau titre Menus")
