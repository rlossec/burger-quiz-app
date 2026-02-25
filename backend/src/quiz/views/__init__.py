"""
ViewSets du module quiz : un ModelViewSet par modèle (un fichier par ressource).
"""

from .question import QuestionViewSet


__all__ = [
    "QuestionViewSet",
]
