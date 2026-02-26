"""
ViewSets du module quiz : un ModelViewSet par modèle (un fichier par ressource).
"""

from .question import QuestionViewSet
from .nugget import NuggetsViewSet
from .salt_or_pepper import SaltOrPepperViewSet

__all__ = [
    "QuestionViewSet",
    "NuggetsViewSet",
    "SaltOrPepperViewSet",
]
