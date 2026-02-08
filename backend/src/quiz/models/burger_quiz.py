
import uuid

from django.db import models


class BurgerQuiz(models.Model):
    class Meta:
        verbose_name_plural = "Burger Quiz"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, null=True, blank=True)
    toss = models.TextField()
    nuggets = models.ForeignKey("Nuggets", on_delete=models.SET_NULL, null=True, blank=True)
    salt_or_pepper = models.ForeignKey("SaltOrPepper", on_delete=models.SET_NULL, null=True, blank=True)
    menus = models.ForeignKey("Menus", on_delete=models.SET_NULL, related_name="burger_quiz", null=True, blank=True)
    addition = models.ForeignKey("Addition", on_delete=models.SET_NULL, null=True, blank=True)
    deadly_burger = models.ForeignKey("DeadlyBurger", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Burger Quiz {self.title}"

    def __repr__(self):
        return f"Burger Quiz {self.title}"