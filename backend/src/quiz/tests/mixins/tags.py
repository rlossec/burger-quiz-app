# Mixins pour les tests du champ tags.

from rest_framework import status

from .base import ResourceTestMixin


class TagsOnCreateMixin(ResourceTestMixin):
    """
    Teste que les tags peuvent être assignés à la création.
    À intégrer dans test_create.py.
    """

    def test_create_with_tags(self):
        """Création avec des tags."""
        payload = self.get_valid_payload()
        payload["tags"] = ["humour", "culture"]

        response = self.client.post(self.get_list_url(), payload, format="json")

        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])
        self.assertIn("tags", response.data)
        self.assertIn("humour", response.data["tags"])
        self.assertIn("culture", response.data["tags"])

    def test_create_without_tags(self):
        """Création sans tags (optionnel)."""
        payload = self.get_valid_payload()
        payload.pop("tags", None)

        response = self.client.post(self.get_list_url(), payload, format="json")

        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])
        self.assertIn("tags", response.data)
        self.assertEqual(len(response.data["tags"]), 0)


class TagsInDetailResponseMixin(ResourceTestMixin):
    """
    Teste que les tags sont présents dans la réponse de détail.
    À intégrer dans test_detail.py.
    """

    def test_tags_in_detail_response(self):
        """Les tags sont présents dans la réponse de détail."""
        instance = self.factory.create(tags=["histoire", "geo"])

        response = self.client.get(self.get_detail_url(instance))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("tags", response.data)
        self.assertIn("histoire", response.data["tags"])
        self.assertIn("geo", response.data["tags"])


class TagsInListResponseMixin(ResourceTestMixin):
    """
    Teste que les tags sont présents dans la réponse de liste.
    À intégrer dans test_list.py.
    """

    def test_tags_in_list_response(self):
        """Les tags sont présents dans la réponse de liste."""
        self.factory.create(tags=["tag1", "tag2"])

        response = self.client.get(self.get_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results", response.data)
        self.assertTrue(len(results) > 0)
        self.assertIn("tags", results[0])


class TagsFilterMixin(ResourceTestMixin):
    """
    Teste le filtrage par tags.
    À intégrer dans test_list.py.
    """

    def test_filter_by_single_tag(self):
        """Filtrage par un seul tag."""
        instance_humour = self.factory.create(tags=["humour"])
        instance_sport = self.factory.create(tags=["sport"])

        response = self.client.get(self.get_list_url(), {"tags": "humour"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [item["id"] for item in response.data.get("results", response.data)]
        self.assertIn(str(instance_humour.id), ids)
        self.assertNotIn(str(instance_sport.id), ids)

    def test_filter_by_multiple_tags(self):
        """Filtrage par plusieurs tags (OR)."""
        instance_humour = self.factory.create(tags=["humour"])
        instance_sport = self.factory.create(tags=["sport"])
        instance_histoire = self.factory.create(tags=["histoire"])

        response = self.client.get(self.get_list_url(), {"tags": "humour,sport"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [item["id"] for item in response.data.get("results", response.data)]
        self.assertIn(str(instance_humour.id), ids)
        self.assertIn(str(instance_sport.id), ids)
        self.assertNotIn(str(instance_histoire.id), ids)


class TagsUpdateMixin(ResourceTestMixin):
    """
    Teste la mise à jour des tags.
    À intégrer dans test_update.py.
    """

    def test_update_tags(self):
        """Mise à jour des tags."""
        instance = self.factory.create(tags=["old-tag"])

        payload = self.get_valid_payload()
        payload["tags"] = ["new-tag", "another"]
        response = self.client.put(self.get_detail_url(instance), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        instance.refresh_from_db()
        tag_names = list(instance.tags.names())
        self.assertIn("new-tag", tag_names)
        self.assertIn("another", tag_names)
        self.assertNotIn("old-tag", tag_names)

    def test_clear_tags(self):
        """Suppression de tous les tags."""
        instance = self.factory.create(tags=["tag1", "tag2"])

        payload = self.get_valid_payload()
        payload["tags"] = []
        response = self.client.put(self.get_detail_url(instance), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        instance.refresh_from_db()
        self.assertEqual(instance.tags.count(), 0)
