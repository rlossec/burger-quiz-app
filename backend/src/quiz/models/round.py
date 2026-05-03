"""
Unified registry of rounds: one line per playable round, with 1–1 link
to exactly one of the concrete models (Nuggets, …).

The `Round.id` is aligned with the concrete round UUID to allow
a simple resolution from the structure (`QuizElement` / `BurgerQuizElement`).
"""

import uuid

from django.core.exceptions import ValidationError
from django.db import models

from .enums import (
    ROUND_TYPE_CHOICES,
    TYPE_ADDITION,
    TYPE_DEADLY_BURGER,
    TYPE_MENUS,
    TYPE_NUGGETS,
    TYPE_SALT_OR_PEPPER,
)


class Round(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    round_type = models.CharField(
        max_length=32,
        choices=ROUND_TYPE_CHOICES,
        verbose_name="type de manche",
    )

    nuggets = models.OneToOneField(
        "Nuggets",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="round_entry",
    )
    salt_or_pepper = models.OneToOneField(
        "SaltOrPepper",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="round_entry",
    )
    menus = models.OneToOneField(
        "Menus",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="round_entry",
    )
    addition = models.OneToOneField(
        "Addition",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="round_entry",
    )
    deadly_burger = models.OneToOneField(
        "DeadlyBurger",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="round_entry",
    )

    class Meta:
        verbose_name = "Manche (registre)"
        verbose_name_plural = "Manches (registre)"

    def __str__(self):
        c = self.concrete
        return f"{self.get_round_type_display()} — {c}"

    def __repr__(self):
        return f"<Round {self.round_type} {self.id}>"

    def clean(self):
        super().clean()
        parts = [
            self.nuggets_id,
            self.salt_or_pepper_id,
            self.menus_id,
            self.addition_id,
            self.deadly_burger_id,
        ]
        if sum(bool(p) for p in parts) != 1:
            raise ValidationError("Exactement une manche concrète doit être liée.")
        if self.nuggets_id and self.round_type != TYPE_NUGGETS.slug:
            raise ValidationError("round_type incohérent avec nuggets.")
        if self.salt_or_pepper_id and self.round_type != TYPE_SALT_OR_PEPPER.slug:
            raise ValidationError("round_type incohérent avec salt_or_pepper.")
        if self.menus_id and self.round_type != TYPE_MENUS.slug:
            raise ValidationError("round_type incohérent avec menus.")
        if self.addition_id and self.round_type != TYPE_ADDITION.slug:
            raise ValidationError("round_type incohérent avec addition.")
        if self.deadly_burger_id and self.round_type != TYPE_DEADLY_BURGER.slug:
            raise ValidationError("round_type incohérent avec deadly_burger.")

    @property
    def concrete(self):
        if self.nuggets_id:
            return self.nuggets
        if self.salt_or_pepper_id:
            return self.salt_or_pepper
        if self.menus_id:
            return self.menus
        if self.addition_id:
            return self.addition
        if self.deadly_burger_id:
            return self.deadly_burger
        return None
