# python manage.py test quiz.tests.menu_themes.test_create
# POST /api/quiz/menu-themes/ — type CL ou TR, questions type ME.

import uuid

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...tests.factories import QuestionFactory, MenuThemeFactory
from ...tests import MENU_TYPE_CL, MENU_TYPE_TR

User = get_user_model()


class TestMenuThemeCreateEndpoint(APITestCase):
    """POST /api/quiz/menu-themes/ — type CL ou TR, questions type ME."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("menu-theme-list")
        self.q1 = QuestionFactory.create_me("ME1")
        self.q2 = QuestionFactory.create_me("ME2")
        self.valid_payload = {
            "title": "Histoire de la gastronomie",
            "type": MENU_TYPE_CL,
            "question_ids": [str(self.q1.id), str(self.q2.id)],
        }

    # 201 Created
    def test_create_menu_theme_classic_success(self):
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["type"], MENU_TYPE_CL)

    def test_create_menu_theme_troll_success(self):
        payload = {**self.valid_payload, "type": MENU_TYPE_TR}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["type"], MENU_TYPE_TR)

    # 400 Bad Request
    def test_create_menu_theme_missing_title(self):
        payload = self.valid_payload.copy()
        payload.pop("title")
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_create_menu_theme_missing_type(self):
        payload = self.valid_payload.copy()
        payload.pop("type")
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("type", response.data)

    def test_create_menu_theme_nonexistent_question_id(self):
        payload = {
            **self.valid_payload,
            "question_ids": [str(self.q1.id), str(uuid.uuid4())],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
