import uuid

from django.db import models


class NuggetQuestion(models.Model):
    """Lien Nuggets ↔ Question avec ordre. Une question (type NU) peut être réutilisée dans plusieurs manches Nuggets."""

    nuggets = models.ForeignKey("Nuggets", on_delete=models.CASCADE)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        unique_together = [["nuggets", "question"]]


class Nuggets(models.Model):
    class Meta:
        verbose_name_plural = "Nuggets"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    original = models.BooleanField(
        default= True,
        help_text="True = créée directement, False = issue d'une émission diffusée.",
    )
    questions = models.ManyToManyField(
        "Question",
        through="NuggetQuestion",
        related_name="nuggets_questions",
        blank=True,
    )

    def __str__(self):
        return f"Nuggets: {self.title}"

    def __repr__(self):
        return f"Nuggets: {self.title}"
