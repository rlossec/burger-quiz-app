# Mixins pour les tests d'authentification requise.

import uuid

from rest_framework import status
from rest_framework.reverse import reverse

from .. import AUTHENTICATION_MISSING


class AuthRequiredMixin:
    """
    Mixin pour tester que l'authentification est requise sur les endpoints.
    
    Attributs à définir :
        - url_basename : basename de l'URL (ex: "salt-or-pepper")
    
    Exemple d'usage dans test_list.py :
        class TestSaltOrPepperListAuthRequired(AuthRequiredMixin, APITestCase):
            url_basename = "salt-or-pepper"
    """
    url_basename = None

    def test_list_requires_authentication(self):
        """GET sur la liste sans auth → 401."""
        self.client.logout()
        url = reverse(f"{self.url_basename}-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], AUTHENTICATION_MISSING)

    def test_create_requires_authentication(self):
        """POST sur la liste sans auth → 401."""
        self.client.logout()
        url = reverse(f"{self.url_basename}-list")
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], AUTHENTICATION_MISSING)

    def test_detail_requires_authentication(self):
        """GET sur un détail sans auth → 401."""
        self.client.logout()
        url = reverse(f"{self.url_basename}-detail", kwargs={"pk": uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], AUTHENTICATION_MISSING)
