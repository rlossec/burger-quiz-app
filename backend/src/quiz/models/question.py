from django.db import models

import uuid

from django.db import models

from .enums import QuestionType


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    question_type = models.CharField(max_length=2, choices=QuestionType.choices)
    explanations = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __repr__(self):
        return self.text[:50]

    def __str__(self):
        return self.text[:50]