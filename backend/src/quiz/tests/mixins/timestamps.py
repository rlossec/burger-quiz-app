# Mixins pour les tests des champs timestamps (created_at, updated_at).

from rest_framework import status

from .base import ResourceTestMixin


class TimestampsInDetailResponseMixin(ResourceTestMixin):
    """
    Teste que les timestamps sont présents dans la réponse de détail.
    À intégrer dans test_detail.py.
    """

    def test_timestamps_in_detail_response(self):
        """created_at et updated_at sont présents dans la réponse de détail."""
        instance = self.factory.create()

        response = self.client.get(self.get_detail_url(instance))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)


class TimestampsInListResponseMixin(ResourceTestMixin):
    """
    Teste que les timestamps sont présents dans la réponse de liste.
    À intégrer dans test_list.py.
    """

    def test_timestamps_in_list_response(self):
        """created_at et updated_at sont présents dans la réponse de liste."""
        self.factory.create()

        response = self.client.get(self.get_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results", response.data)
        self.assertTrue(len(results) > 0)
        self.assertIn("created_at", results[0])
        self.assertIn("updated_at", results[0])


class TimestampsReadOnlyMixin(ResourceTestMixin):
    """
    Teste que les timestamps ne peuvent pas être modifiés.
    À intégrer dans test_create.py.
    """

    def test_timestamps_are_readonly(self):
        """created_at et updated_at ne peuvent pas être définis manuellement."""
        payload = self.get_valid_payload()
        payload.setdefault("tags", [])
        payload["created_at"] = "2020-01-01T00:00:00Z"
        payload["updated_at"] = "2020-01-01T00:00:00Z"

        response = self.client.post(self.get_list_url(), payload, format="json")

        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])
        self.assertNotEqual(response.data.get("created_at"), "2020-01-01T00:00:00Z")
