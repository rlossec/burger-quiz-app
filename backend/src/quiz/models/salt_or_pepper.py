import uuid

from django.db import models


class SaltOrPepperQuestion(models.Model):
    """Lien SaltOrPepper ↔ Question avec ordre pour la manche."""

    salt_or_pepper = models.ForeignKey("SaltOrPepper", on_delete=models.CASCADE)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        unique_together = [["salt_or_pepper", "question"]]


class SaltOrPepper(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
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