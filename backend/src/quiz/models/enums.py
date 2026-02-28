from django.db import models


class QuestionType(models.TextChoices):
    NU = "NU", "Nuggets"
    SP = "SP", "Sel ou Poivre"
    ME = "ME", "Menu"
    AD = "AD", "Addition"
    DB = "DB", "Burger de la Mort"


class InterludeType(models.TextChoices):
    IN = "IN", "Intro"
    OU = "OU", "Outro"
    PU = "PU", "Pub"
    IL = "IL", "Interlude"


class ElementType(models.TextChoices):
    ROUND = "round", "Manche"
    INTERLUDE = "interlude", "Interlude"
