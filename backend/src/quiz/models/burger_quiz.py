import uuid

from django.db import models

from .base import QuizContentMixin


class BurgerQuiz(QuizContentMixin, models.Model):

    class Meta:
        verbose_name_plural = "Burger Quiz"
        ordering = ["-created_at"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, null=True, blank=True)
    toss = models.TextField()

    def __str__(self):
        return f"Burger Quiz {self.title}"

    def __repr__(self):
        return f"Burger Quiz {self.title}"
