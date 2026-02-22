import uuid

from django.db import models


class AdditionQuestion(models.Model):
    """Lien Addition ↔ Question avec ordre. Une question (type AD) n'appartient qu'à une seule Addition."""

    addition = models.ForeignKey("Addition", on_delete=models.CASCADE)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        unique_together = [["addition", "question"]]
        constraints = [
            models.UniqueConstraint(fields=["question"], name="unique_question_addition"),
        ]


class Addition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    original = models.BooleanField(
        default=True,
        help_text="True = créée directement, False = issue d'une émission diffusée.",
    )
    questions = models.ManyToManyField(
        "Question",
        through="AdditionQuestion",
        related_name="addition_questions",
        blank=True,
    )

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title