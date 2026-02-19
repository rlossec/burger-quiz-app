# python manage.py test quiz.tests.additions.test_update
# PATCH / PUT /api/quiz/additions/{id}/.

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...tests.factories import AdditionFactory


class TestAdditionUpdateEndpoint(APITestCase):
    """PATCH / PUT /api/quiz/additions/{id}/."""

    def setUp(self):
        self.addition = AdditionFactory.create(title="Addition à modifier", original=False)
        self.url = reverse("addition-detail", kwargs={"pk": self.addition.pk})

    # 200 OK
    def test_patch_additions_title_success(self):
        response = self.client.patch(
            self.url, {"title": "Nouvelle addition"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Nouvelle addition")
