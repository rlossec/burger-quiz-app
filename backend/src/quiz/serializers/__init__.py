"""
Serializers du module quiz : un fichier par modèle.
"""

from .answer import AnswerSerializer
from .question import QuestionSerializer, QuestionListSerializer
from .nugget import NuggetsSerializer
from .salt_or_pepper import SaltOrPepperSerializer
from .menus import MenusSerializer
from .menu_theme import MenuThemeSerializer

__all__ = [
    "AnswerSerializer",
    "QuestionSerializer",
    "QuestionListSerializer",
    "NuggetsSerializer",
    "SaltOrPepperSerializer",
    "MenusSerializer",
    "MenuThemeSerializer",
]
