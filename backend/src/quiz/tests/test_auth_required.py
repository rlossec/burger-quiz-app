# python manage.py test quiz.tests.test_auth_required
# Vérifie que toutes les routes quiz sont privées : requête sans auth → 401.

import uuid

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from . import AUTHENTICATION_MISSING


# (basename du routeur quiz/urls.py, libellé pour les messages)
QUIZ_BASENAMES = [
    ("question", "questions"),
    ("nuggets", "nuggets"),
    ("salt-or-pepper", "salt-or-pepper"),
    ("menu-theme", "menu-themes"),
    ("menus", "menus"),
    ("addition", "additions"),
    ("deadly-burger", "deadly-burgers"),
    ("burger-quiz", "burger-quizzes"),
]


class TestQuizEndpointsRequireAuth(APITestCase):
    """
    Toutes les routes quiz exigent une authentification (JWT).
    Sans credentials, la API renvoie 401 avec le message DRF attendu.
    """

    def test_list_endpoints_require_authentication(self):
        """GET sur chaque liste sans auth → 401."""
        for basename, _ in QUIZ_BASENAMES:
            with self.subTest(basename=basename):
                url = reverse(f"{basename}-list")
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code,
                    status.HTTP_401_UNAUTHORIZED,
                    f"GET {url} sans auth doit renvoyer 401",
                )
                self.assertIn("detail", response.data)
                self.assertEqual(
                    response.data["detail"],
                    AUTHENTICATION_MISSING,
                    "Message DRF attendu pour credentials manquants",
                )

    def test_create_endpoints_require_authentication(self):
        """POST sur chaque liste sans auth → 401 (permission vérifiée avant validation)."""
        for basename, _ in QUIZ_BASENAMES:
            with self.subTest(basename=basename):
                url = reverse(f"{basename}-list")
                response = self.client.post(url, {}, format="json")
                self.assertEqual(
                    response.status_code,
                    status.HTTP_401_UNAUTHORIZED,
                    f"POST {url} sans auth doit renvoyer 401",
                )
                self.assertIn("detail", response.data)
                self.assertEqual(
                    response.data["detail"],
                    AUTHENTICATION_MISSING,
                )

    def test_detail_endpoints_require_authentication(self):
        """GET sur un détail (pk quelconque) sans auth → 401."""
        fake_pk = uuid.uuid4()
        for basename, _ in QUIZ_BASENAMES:
            with self.subTest(basename=basename):
                url = reverse(f"{basename}-detail", kwargs={"pk": fake_pk})
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code,
                    status.HTTP_401_UNAUTHORIZED,
                    f"GET {url} sans auth doit renvoyer 401",
                )
                self.assertIn("detail", response.data)
                self.assertEqual(
                    response.data["detail"],
                    AUTHENTICATION_MISSING,
                )
