"""
ViewSets du module quiz : un ModelViewSet par modèle (un fichier par ressource).
"""

from .question import QuestionViewSet
from .nugget import NuggetsViewSet

__all__ = [
    "QuestionViewSet",
    "NuggetsViewSet",
]
