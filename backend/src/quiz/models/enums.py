from django.db import models


class QuestionType(models.TextChoices):
    NU = "NU", "Nuggets"
    SP = "SP", "Sel ou Poivre"
    ME = "ME", "Menu"
    AD = "AD", "Addition"
    DB = "DB", "Burger de la Mort"
