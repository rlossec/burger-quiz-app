"""
Mixins réutilisables pour les vues quiz.
"""


class AuthorAutoAssignMixin:
    """
    Mixin pour auto-assigner l'auteur lors de la création.
    L'auteur est extrait du JWT de la requête.
    """

    def perform_create(self, serializer):
        """Assigne automatiquement l'utilisateur connecté comme auteur."""
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)
        else:
            serializer.save()
