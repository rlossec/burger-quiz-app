import uuid

from django.db import models
from django.core.exceptions import ValidationError


class BurgerQuizElement(models.Model):
    """
    Ordered position of a content in the Burger Quiz structure.
    Either a round or a video interlude.
    """

    class ElementType(models.TextChoices):
        ROUND = "round", "Manche"
        INTERLUDE = "interlude", "Interlude vidéo"

    class Meta:
        verbose_name = "Élément de Burger Quiz"
        verbose_name_plural = "Éléments de Burger Quiz"
        ordering = ["burger_quiz", "order"]
        unique_together = [
            ("burger_quiz", "order"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    burger_quiz = models.ForeignKey(
        "BurgerQuiz",
        on_delete=models.CASCADE,
        related_name="structure_elements",
        verbose_name="Burger Quiz",
    )
    order = models.PositiveIntegerField(verbose_name="Ordre")
    element_type = models.CharField(
        max_length=20,
        choices=ElementType.choices,
        verbose_name="Type d'élément",
    )
    round = models.ForeignKey(
        "Round",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="structure_usages",
        verbose_name="Manche (registre)",
    )
    interlude = models.ForeignKey(
        "VideoInterlude",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="structure_usages",
        verbose_name="Interlude vidéo",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.order} {self.content}"

    def __repr__(self):
        return f"<BurgerQuizElement {self.burger_quiz_id} #{self.order}>"

    def clean(self):
        super().clean()
        if self.element_type == self.ElementType.ROUND:
            if self.round_id is None or self.interlude_id is not None:
                raise ValidationError(
                    "Pour une manche, `round` est requis et `interlude` doit être vide."
                )
        elif self.element_type == self.ElementType.INTERLUDE:
            if self.interlude_id is None or self.round_id is not None:
                raise ValidationError(
                    "Pour un interlude, `interlude` est requis et `round` doit être vide."
                )

    @property
    def content(self):
        """Concrete round or video interlude. Uses already loaded FKs (select_related), without additional query."""
        if self.element_type == self.ElementType.INTERLUDE:
            return self.interlude
        if self.element_type == self.ElementType.ROUND and self.round_id and self.round:
            r = self.round
            return (
                r.nuggets
                or r.salt_or_pepper
                or r.menus
                or r.addition
                or r.deadly_burger
            )
        return None
