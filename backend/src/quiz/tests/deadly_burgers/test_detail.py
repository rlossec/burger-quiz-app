# python manage.py test quiz.tests.deadly_burgers.test_detail
# GET /api/quiz/deadly-burgers/{id}/ — Détail.

import uuid

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...tests.factories import DeadlyBurgerFactory


class TestDeadlyBurgerDetailEndpoint(APITestCase):
    """GET /api/quiz/deadly-burgers/{id}/ — Détail."""

    def setUp(self):
        self.db = DeadlyBurgerFactory.create(
            title="Burger de la mort - Finale", original=False
        )
        self.url = reverse("deadly-burger-detail", kwargs={"pk": self.db.pk})

    # 200 OK
    def test_detail_deadly_burgers_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), self.db.title)
        self.assertEqual(response.data.get("original"), self.db.original)

    # 404 Not Found
    def test_detail_deadly_burgers_not_found(self):
        url = reverse("deadly-burger-detail", kwargs={"pk": uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
