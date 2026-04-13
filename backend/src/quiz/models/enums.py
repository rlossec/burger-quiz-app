
from typing import NamedTuple

from django.db import models


class RoundTypeSpec(NamedTuple):
    """An entry in the catalog: round slug/API, question code, label, FK to Round."""

    slug: str
    question_code: str
    label: str
    round_fk: str


ROUND_SPECS: tuple[RoundTypeSpec, ...] = (
    RoundTypeSpec("nuggets", "NU", "Nuggets", "nuggets"),
    RoundTypeSpec("salt_or_pepper", "SP", "Sel ou Poivre", "salt_or_pepper"),
    RoundTypeSpec("menus", "ME", "Menus", "menus"),
    RoundTypeSpec("addition", "AD", "Addition", "addition"),
    RoundTypeSpec("deadly_burger", "DB", "Burger de la Mort", "deadly_burger"),
)

ROUND_TYPE_CHOICES = tuple((s.slug, s.label) for s in ROUND_SPECS)
QUESTION_TYPE_CHOICES = tuple((s.question_code, s.label) for s in ROUND_SPECS)

_BY_ROUND_SLUG = {s.slug: s for s in ROUND_SPECS}
_BY_QUESTION_CODE = {s.question_code: s for s in ROUND_SPECS}

_q = _BY_QUESTION_CODE


def question_code_for_round_slug(slug: str) -> str:
    """Code QuestionType (ex. NU) pour un slug round (ex. nuggets)."""
    return _BY_ROUND_SLUG[slug].question_code


def round_slug_for_question_code(question_code: str) -> str:
    """Slug round pour un code question (ex. NU → nuggets)."""
    return _BY_QUESTION_CODE[question_code].slug


def type_for_round_slug(slug: str) -> RoundTypeSpec:
    return _BY_ROUND_SLUG[slug]


def type_for_question_code(question_code: str) -> RoundTypeSpec:
    return _BY_QUESTION_CODE[question_code]


(
    TYPE_NUGGETS,
    TYPE_SALT_OR_PEPPER,
    TYPE_MENUS,
    TYPE_ADDITION,
    TYPE_DEADLY_BURGER,
) = ROUND_SPECS


class QuestionType(models.TextChoices):
    """Codes questions (champ Question.question_type) — libellés alignés sur ROUND_SPECS."""

    NU = _q["NU"].question_code, _q["NU"].label
    SP = _q["SP"].question_code, _q["SP"].label
    ME = _q["ME"].question_code, _q["ME"].label
    AD = _q["AD"].question_code, _q["AD"].label
    DB = _q["DB"].question_code, _q["DB"].label
