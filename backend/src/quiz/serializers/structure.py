"""
Aide à la structure d'un Burger Quiz : types API, sérialisation, ordre par lignes BurgerQuizElement.
"""

from __future__ import annotations

import uuid
from typing import Any

from rest_framework.serializers import ValidationError

from ..models import (
    Addition,
    BurgerQuiz,
    DeadlyBurger,
    Menus,
    Nuggets,
    SaltOrPepper,
    VideoInterlude,
)

from .addition import AdditionSerializer
from .deadly_burger import DeadlyBurgerSerializer
from .menus import MenusSerializer
from .nugget import NuggetsSerializer
from .salt_or_pepper import SaltOrPepperSerializer
from .video_interlude import VideoInterludeSerializer


# type API (slug) -> classe modèle
STRUCTURE_TYPE_TO_MODEL: dict[str, type] = {
    "nuggets": Nuggets,
    "salt_or_pepper": SaltOrPepper,
    "menus": Menus,
    "addition": Addition,
    "deadly_burger": DeadlyBurger,
    "video_interlude": VideoInterlude,
}

MODEL_TO_SLUG: dict[type, str] = {
    Nuggets: "nuggets",
    SaltOrPepper: "salt_or_pepper",
    Menus: "menus",
    Addition: "addition",
    DeadlyBurger: "deadly_burger",
    VideoInterlude: "video_interlude",
}

STRUCTURE_TYPE_TO_SERIALIZER: dict[str, type] = {
    "nuggets": NuggetsSerializer,
    "salt_or_pepper": SaltOrPepperSerializer,
    "menus": MenusSerializer,
    "addition": AdditionSerializer,
    "deadly_burger": DeadlyBurgerSerializer,
    "video_interlude": VideoInterludeSerializer,
}


def parse_structure_element(raw: dict[str, Any]) -> tuple[str, uuid.UUID]:
    """
    Retourne (slug_api, object_id) depuis un objet du tableau elements du PUT.
    Forme unique : {"type": "nuggets"|"video_interlude"|…, "id": "uuid"}
    Lève ValidationError (DRF) pour des réponses 400 cohérentes.
    """
    t = raw.get("type")
    if t is None:
        raise ValidationError({"elements": "Le champ type est requis."})

    t_norm = str(t).strip().lower()
    if t_norm not in STRUCTURE_TYPE_TO_MODEL:
        raise ValidationError({"elements": f"Type d'élément inconnu : {t!r}."})

    eid = raw.get("id")
    if not eid:
        raise ValidationError({"elements": f"Pour type={t_norm!r}, id est requis."})
    try:
        return t_norm, uuid.UUID(str(eid))
    except ValueError:
        raise ValidationError({"elements": f"id invalide pour type={t_norm!r}."}) from None


def structure_elements_to_representation(
    burger_quiz: BurgerQuiz,
    *,
    expand_full: bool = False,
) -> list[dict[str, Any]]:
    """
    Liste pour GET structure / champ structure du détail.
    Si expand_full=False : {order, type, id} seulement.
    Si expand_full=True : objets complets sous la clé du type (nuggets, video_interlude, …).
    """
    rows = list(
        burger_quiz.structure_elements.select_related(
            "round",
            "interlude",
            "round__nuggets",
            "round__salt_or_pepper",
            "round__menus",
            "round__addition",
            "round__deadly_burger",
        ).order_by("order")
    )
    if not rows:
        return []

    result: list[dict[str, Any]] = []
    for row in rows:
        obj = row.content
        if obj is None:
            continue
        slug = MODEL_TO_SLUG.get(type(obj), "unknown")
        item: dict[str, Any] = {
            "order": row.order,
            "type": slug,
            "id": str(obj.id),
        }
        if expand_full:
            serializer_class = STRUCTURE_TYPE_TO_SERIALIZER.get(slug)
            if serializer_class is not None:
                item[slug] = serializer_class(obj).data
        result.append(item)
    return result
