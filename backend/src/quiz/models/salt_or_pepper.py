import uuid

from django.db import models


class SaltOrPepperQuestion(models.Model):
    """Lien SaltOrPepper ↔ Question avec ordre. Une question (type SP) n'appartient qu'à un seul Sel ou poivre."""

    salt_or_pepper = models.ForeignKey("SaltOrPepper", on_delete=models.CASCADE)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        unique_together = [["salt_or_pepper", "question"]]
        constraints = [
            models.UniqueConstraint(fields=["question"], name="unique_question_salt_or_pepper"),
        ]


class SaltOrPepper(models.Model):
    """Manche Sel ou Poivre : les réponses de chaque question sont parmi une liste restreinte (souvent 2–4, max 5)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    original = models.BooleanField(
        default= True,
        help_text="True = créée directement, False = issue d'une émission diffusée.",
    )
    choice_labels = models.JSONField(
        default=list,
        help_text="Liste des propositions (ex. ['Noir', 'Blanc'] ou ['Noir', 'Blanc', 'Les deux']). Entre 2 et 5 libellés.",
    )
    questions = models.ManyToManyField(
        "Question",
        through="SaltOrPepperQuestion",
        related_name="salt_or_pepper_questions",
        blank=True,
    )

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title