# Mixins pour les tests du champ author.

from rest_framework import status

from .base import ResourceTestMixin
from ..factories import UserFactory


class AuthorAutoAssignOnCreateMixin(ResourceTestMixin):
    """
    Teste que l'auteur est automatiquement assigné à la création.
    À intégrer dans test_create.py.
    """

    def test_author_auto_assigned_on_create(self):
        """L'auteur est automatiquement assigné à l'utilisateur connecté."""
        payload = self.get_valid_payload()
        payload.setdefault("tags", [])

        response = self.client.post(self.get_list_url(), payload, format="json")

        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])
        self.assertIn("author", response.data)
        self.assertIsNotNone(response.data["author"])
        self.assertEqual(response.data["author"]["id"], self.user.id)
        self.assertEqual(response.data["author"]["username"], self.user.username)


class AuthorReadOnlyOnCreateMixin(ResourceTestMixin):
    """
    Teste que l'auteur ne peut pas être défini manuellement à la création.
    À intégrer dans test_create.py.
    """

    def test_author_cannot_be_set_manually_on_create(self):
        """Le champ author est ignoré s'il est fourni dans le payload."""
        other_user = UserFactory.create(username="other_user_author")
        payload = self.get_valid_payload()
        payload.setdefault("tags", [])
        payload["author"] = {"id": other_user.id, "username": other_user.username}

        response = self.client.post(self.get_list_url(), payload, format="json")

        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])
        self.assertEqual(response.data["author"]["id"], self.user.id)
        self.assertNotEqual(response.data["author"]["id"], other_user.id)


class AuthorInDetailResponseMixin(ResourceTestMixin):
    """
    Teste que l'auteur est présent dans la réponse de détail.
    À intégrer dans test_detail.py.
    """

    def test_author_in_detail_response(self):
        """L'auteur est présent dans la réponse de détail."""
        instance = self.factory.create(author=self.user)

        response = self.client.get(self.get_detail_url(instance))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("author", response.data)
        self.assertIsNotNone(response.data["author"])
        self.assertEqual(response.data["author"]["id"], self.user.id)


class AuthorInListResponseMixin(ResourceTestMixin):
    """
    Teste que l'auteur est présent dans la réponse de liste.
    À intégrer dans test_list.py.
    """

    def test_author_in_list_response(self):
        """L'auteur est présent dans la réponse de liste."""
        self.factory.create(author=self.user)

        response = self.client.get(self.get_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results", response.data)
        self.assertTrue(len(results) > 0)
        self.assertIn("author", results[0])


class AuthorFilterMixin(ResourceTestMixin):
    """
    Teste le filtrage par auteur.
    À intégrer dans test_list.py.
    """

    def test_filter_by_author(self):
        """Filtrage des ressources par author."""
        other_user = UserFactory.create(username="other_user_filter")
        instance_user = self.factory.create(author=self.user)
        instance_other = self.factory.create(author=other_user)

        response = self.client.get(self.get_list_url(), {"author": self.user.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [item["id"] for item in response.data.get("results", response.data)]
        self.assertIn(str(instance_user.id), ids)
        self.assertNotIn(str(instance_other.id), ids)


class AuthorNotChangedOnUpdateMixin(ResourceTestMixin):
    """
    Teste que l'auteur ne change pas lors d'une mise à jour.
    À intégrer dans test_update.py.
    """

    def test_author_not_changed_on_update(self):
        """L'auteur ne change pas lors d'une mise à jour."""
        instance = self.factory.create(author=self.user)

        payload = self.get_valid_payload()
        payload.setdefault("tags", [])
        response = self.client.put(self.get_detail_url(instance), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        instance.refresh_from_db()
        self.assertEqual(instance.author, self.user)
