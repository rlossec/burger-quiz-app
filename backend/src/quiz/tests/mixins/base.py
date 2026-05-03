# Classe de base pour les mixins de test.
# Définit les attributs communs à configurer dans chaque classe de test.

from rest_framework.reverse import reverse


class ResourceTestMixin:
    """
    Mixin de base fournissant les helpers pour les tests de ressources.
    
    Attributs à définir dans la classe de test :
        - factory : DjangoModelFactory pour créer des instances
        - url_basename : basename de l'URL (ex: "salt-or-pepper")
        - valid_payload : dict ou callable retournant le payload de création valide
    
    Exemple :
        class TestSaltOrPepperCreate(AuthorAutoAssignOnCreateMixin, APITestCase):
            factory = SaltOrPepperFactory
            url_basename = "salt-or-pepper"
            valid_payload = {"title": "Test", "propositions": ["A", "B"]}
    """
    factory = None
    url_basename = None
    valid_payload = None

    def get_valid_payload(self):
        """Retourne le payload de création valide (gère dict ou callable)."""
        if callable(self.valid_payload):
            return self.valid_payload()
        return self.valid_payload.copy() if self.valid_payload else {}

    def get_list_url(self):
        """Retourne l'URL de liste."""
        return reverse(f"{self.url_basename}-list")

    def get_detail_url(self, instance):
        """Retourne l'URL de détail pour une instance."""
        return reverse(f"{self.url_basename}-detail", kwargs={"pk": instance.pk})
