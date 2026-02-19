# python manage.py test quiz.tests.additions.test_detail
# GET /api/quiz/additions/{id}/ — Détail.

import uuid

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...tests.factories import AdditionFactory


class TestAdditionDetailEndpoint(APITestCase):
    """GET /api/quiz/additions/{id}/ — Détail."""

    def setUp(self):
        self.addition = AdditionFactory.create(title="Addition rapide", original=False)
        self.url = reverse("addition-detail", kwargs={"pk": self.addition.pk})

    # 200 OK
    def test_detail_additions_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), self.addition.title)
        self.assertEqual(response.data.get("original"), self.addition.original)

    # 404 Not Found
    def test_detail_additions_not_found(self):
        url = reverse("addition-detail", kwargs={"pk": uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
