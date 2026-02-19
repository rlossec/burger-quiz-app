# python manage.py test quiz.tests.menus.test_create
# POST /api/quiz/menus/ — 2 classiques + 1 troll, IDs distincts.

import uuid

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...models import Menus
from ...tests.factories import MenuThemeFactory


class TestMenusCreateEndpoint(APITestCase):
    """POST /api/quiz/menus/ — 2 classiques + 1 troll, IDs distincts."""

    def setUp(self):
        self.url = reverse("menus-list")
        self.theme_1 = MenuThemeFactory.create_classic(title="CL 1")
        self.theme_2 = MenuThemeFactory.create_classic(title="CL 2")
        self.theme_troll = MenuThemeFactory.create_troll(title="TR 1")
        self.valid_payload = {
            "title": "Menus du jour",
            "description": "Optionnel",
            "original": False,
            "menu_1_id": str(self.theme_1.id),
            "menu_2_id": str(self.theme_2.id),
            "menu_troll_id": str(self.theme_troll.id),
        }

    # 201 Created
    def test_create_menus_success(self):
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["title"], self.valid_payload["title"])
        m = Menus.objects.get(title=self.valid_payload["title"])
        self.assertEqual(m.menu_1_id, self.theme_1.id)
        self.assertEqual(m.menu_2_id, self.theme_2.id)
        self.assertEqual(m.menu_troll_id, self.theme_troll.id)

    # 400 Bad Request
    def test_create_menus_missing_title(self):
        payload = self.valid_payload.copy()
        payload.pop("title")
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_create_menus_menu_1_not_classic(self):
        troll2 = MenuThemeFactory.create_troll(title="TR 2")
        payload = {**self.valid_payload, "menu_1_id": str(troll2.id)}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_menus_menu_troll_not_troll(self):
        payload = {**self.valid_payload, "menu_troll_id": str(self.theme_1.id)}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_menus_same_theme_twice(self):
        payload = {**self.valid_payload, "menu_2_id": str(self.theme_1.id)}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_menus_nonexistent_theme_id(self):
        payload = {**self.valid_payload, "menu_troll_id": str(uuid.uuid4())}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
