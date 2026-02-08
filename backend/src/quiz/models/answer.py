import uuid

from django.db import models


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey("Question", on_delete=models.CASCADE, related_name="answers")
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    image = models.ImageField(upload_to="answers/", blank=True, null=True)

    def __str__(self):
        return self.text[:50]