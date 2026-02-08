import uuid

from django.db import models


class MenuThemeQuestion(models.Model):
    """Lien MenuTheme ↔ Question avec ordre pour la série."""

    menu_theme = models.ForeignKey("MenuTheme", on_delete=models.CASCADE)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        unique_together = [["menu_theme", "question"]]


class MenuTheme(models.Model):
    MENU_TYPES = [
        ("TR", "Troll"),
        ("CL", "Classique"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=2, choices=MENU_TYPES, default="CL")
    questions = models.ManyToManyField(
        "Question",
        through="MenuThemeQuestion",
        related_name="menu_questions",
        blank=True,
    )

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title

class Menus(models.Model):

    class Meta:
        verbose_name_plural = "Menus"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    menu_1 = models.ForeignKey("MenuTheme", on_delete=models.SET_NULL, null=True, blank=True, related_name="menus_as_menu_1")
    menu_2 = models.ForeignKey("MenuTheme", on_delete=models.SET_NULL, null=True, blank=True, related_name="menus_as_menu_2")
    menu_troll = models.ForeignKey("MenuTheme", on_delete=models.SET_NULL, null=True, blank=True, related_name="menus_as_menu_troll")

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title
