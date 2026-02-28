"""
Serializers du module quiz : un fichier par modèle.
"""

from .answer import AnswerSerializer
from .question import QuestionSerializer, QuestionListSerializer
from .nugget import NuggetsSerializer
from .salt_or_pepper import SaltOrPepperSerializer
from .menus import MenusSerializer
from .menu_theme import MenuThemeSerializer
from .addition import AdditionSerializer
from .deadly_burger import DeadlyBurgerSerializer
from .video_interlude import (
    VideoInterludeSerializer,
    VideoInterludeListSerializer,
    VideoInterludeMinimalSerializer,
)
from .burger_quiz_element import (
    BurgerQuizElementReadSerializer,
    BurgerQuizElementWriteSerializer,
    BurgerQuizStructureSerializer,
    BurgerQuizStructureReadSerializer,
)
from .burger_quiz import BurgerQuizSerializer

__all__ = [
    "AnswerSerializer",
    "QuestionSerializer",
    "QuestionListSerializer",
    "NuggetsSerializer",
    "SaltOrPepperSerializer",
    "MenusSerializer",
    "MenuThemeSerializer",
    "AdditionSerializer",
    "DeadlyBurgerSerializer",
    "VideoInterludeSerializer",
    "VideoInterludeListSerializer",
    "VideoInterludeMinimalSerializer",
    "BurgerQuizElementReadSerializer",
    "BurgerQuizElementWriteSerializer",
    "BurgerQuizStructureSerializer",
    "BurgerQuizStructureReadSerializer",
    "BurgerQuizSerializer",
]
