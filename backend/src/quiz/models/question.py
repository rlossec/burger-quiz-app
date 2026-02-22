import uuid

from django.db import models

from .enums import QuestionType


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    question_type = models.CharField(max_length=2, choices=QuestionType.choices)
    original = models.BooleanField(
        default=True,
        help_text="True = créée directement, False = issue d'une émission diffusée.",
    )
    explanations = models.TextField(blank=True, null=True)
    video_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Lien externe vers une vidéo (ex. extrait d'émission).",
    )
    image_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Lien externe vers une image.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return self.text[:50]

    def __str__(self):
        return self.text[:50]