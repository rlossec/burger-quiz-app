"""
ViewSets du module quiz : un ModelViewSet par modèle (un fichier par ressource).
"""

from .question import QuestionViewSet
from .nugget import NuggetsViewSet
from .salt_or_pepper import SaltOrPepperViewSet
from .menus import MenusViewSet
from .menu_theme import MenuThemeViewSet
from .addition import AdditionViewSet
from .deadly_burger import DeadlyBurgerViewSet
from .burger_quiz import BurgerQuizViewSet

__all__ = [
    "QuestionViewSet",
    "NuggetsViewSet",
    "SaltOrPepperViewSet",
    "MenusViewSet",
    "MenuThemeViewSet",
    "AdditionViewSet",
    "DeadlyBurgerViewSet",
    "BurgerQuizViewSet",
]
