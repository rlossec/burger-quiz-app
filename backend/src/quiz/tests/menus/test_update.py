# python manage.py test quiz.tests.menus.test_update
# PATCH / PUT /api/quiz/menus/{id}/.

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...tests.factories import MenusFactory


class TestMenusUpdateEndpoint(APITestCase):
    """PATCH / PUT /api/quiz/menus/{id}/."""

    def setUp(self):
        self.menus = MenusFactory.create(title="Menus à modifier", original=False)
        self.url = reverse("menus-detail", kwargs={"pk": self.menus.pk})

    # 200 OK
    def test_patch_menus_title_success(self):
        response = self.client.patch(
            self.url, {"title": "Nouveau titre Menus"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Nouveau titre Menus")
