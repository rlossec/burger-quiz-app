import uuid

from django.db import models


class DeadlyBurgerQuestion(models.Model):
    """Lien DeadlyBurger ↔ Question avec ordre (10 questions). Une question (type DB) peut être réutilisée dans plusieurs Burger de la mort."""

    deadly_burger = models.ForeignKey("DeadlyBurger", on_delete=models.CASCADE)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        unique_together = [["deadly_burger", "question"]]


class DeadlyBurger(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    original = models.BooleanField(
        default=True,
        help_text="True = créée directement, False = issue d'une émission diffusée.",
    )
    questions = models.ManyToManyField(
        "Question",
        through="DeadlyBurgerQuestion",
        related_name="deadly_burgers",
        blank=True,
    )

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title
