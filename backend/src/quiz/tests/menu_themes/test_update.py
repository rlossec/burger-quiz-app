# python manage.py test quiz.tests.menu_themes.test_update
# PATCH / PUT /api/quiz/menu-themes/{id}/.

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...tests.factories import MenuThemeFactory

User = get_user_model()


class TestMenuThemeUpdateEndpoint(APITestCase):
    """PATCH / PUT /api/quiz/menu-themes/{id}/."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.theme = MenuThemeFactory.create_classic(title="Thème à modifier")
        self.url = reverse("menu-theme-detail", kwargs={"pk": self.theme.pk})

    # 200 OK
    def test_patch_menu_theme_title_success(self):
        response = self.client.patch(
            self.url, {"title": "Nouveau titre thème"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Nouveau titre thème")
