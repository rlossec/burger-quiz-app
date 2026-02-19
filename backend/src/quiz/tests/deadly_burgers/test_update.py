# python manage.py test quiz.tests.deadly_burgers.test_update
# PATCH / PUT /api/quiz/deadly-burgers/{id}/.

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...tests.factories import DeadlyBurgerFactory


class TestDeadlyBurgerUpdateEndpoint(APITestCase):
    """PATCH / PUT /api/quiz/deadly-burgers/{id}/."""

    def setUp(self):
        self.db = DeadlyBurgerFactory.create_with_ten_questions(title="DB à modifier")
        self.url = reverse("deadly-burger-detail", kwargs={"pk": self.db.pk})

    # 200 OK
    def test_patch_deadly_burgers_title_success(self):
        response = self.client.patch(
            self.url, {"title": "Nouveau Burger de la mort"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Nouveau Burger de la mort")
